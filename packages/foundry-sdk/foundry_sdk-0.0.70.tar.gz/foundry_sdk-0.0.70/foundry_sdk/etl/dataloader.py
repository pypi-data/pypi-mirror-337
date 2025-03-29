from foundry_sdk.db_mgmt import SQLDatabase, InsertionMode
from foundry_sdk.db_mgmt.tables import *
from foundry_sdk.db_mgmt.data_retrieval import retrieve_data
from foundry_sdk.etl.validation import *
from foundry_sdk.utils import convert_to_df
from foundry_sdk.etl.data_retrieval.data_filters import get_data_ids_by_company, get_data_ids
from foundry_sdk.etl.data_insertion import handle_time_sku_table_creation

import typing as t
import pandas as pd
import numpy as np
from tqdm import tqdm

import logging
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading of data into the database using the write_* methods."""

    def __init__(self, db: SQLDatabase, insertion_mode: str):
        """
        Args:
            db (SQLDatabase): Database connection object.
            insertion_mode (InsertionMode): Mode for database insertion.
        """
        self.db = db
        self.insertion_mode = insertion_mode
    
    #################################### Mandatory data ############################################

    def write_company(self, name: str, dataset_type: str, description: str, min_date: pd.Timestamp, max_date: pd.Timestamp) -> Company:
        
        """Create and write a company to the database.

        Args:
            name (str): Company name.
            dataset_type (str): Dataset type.
            description (str): Company description.

        Returns:
            Company: The created company.
        """

        check_company_inputs(name, dataset_type, description, min_date, max_date)

        company = Company(self.db, self.insertion_mode)
        company.write_to_db_single_row(name, dataset_type, description, min_date, max_date, save_ids=True)
        
        return company

    def write_stores(
        self, store_region_map: pd.DataFrame, company: Company
    ) -> Stores:
        """Create and write store entries to the database.

        Args:
            store_region_map (dict): Mapping of store identifiers to regions.
            regions (Regions): Regions object.
            company (Company): Company object.

        Returns:
            Stores: The created Stores object.
        """

        store_regions_adjusted = clean_and_check_store_region_map(store_region_map, copy=True)
        columns = store_regions_adjusted.columns

        
        for column in columns:
            if column in ["store", "country"]:
                continue
            region_type = column
    
        countries = store_regions_adjusted["country"].unique()
        country_id_map = dict()
        for country in countries:
            country_id = retrieve_data(self.db, "regions", "ID", f"abbreviation='{country}' AND type='country'")
            if not country_id:
                raise ValueError(f"Country {country} not found in the database. Ensure the General Data pipeline is executed first. See step 3 in: https://github.com/d3group/foundry-master/blob/main/documentation/new_db_set_up.md")
            else:
                country_id = country_id[0][0]
            country_id_map[country] = country_id

        store_regions_adjusted["countryID"] = store_regions_adjusted["country"].map(country_id_map)

        if len(columns) == 2:
            # rename countryID to regionID
            store_regions_adjusted.rename(columns={"countryID": "regionID"}, inplace=True)
            del store_regions_adjusted["country"]

        else:
            country_chunk_data = []
            for country in countries:
                country_data = store_regions_adjusted[store_regions_adjusted["country"] == country]
                sub_region_id_map = dict()
                for sub_region in country_data[region_type].unique():
                    region_id = retrieve_data(self.db, "regions", "ID", f"country={country_id} AND abbreviation='{sub_region}' AND type = '{region_type}'")[0][0]
                    sub_region_id_map[sub_region] = region_id
                country_data[f"regionID"] = country_data[region_type].map(sub_region_id_map)
                country_chunk_data.append(country_data)
            
            store_regions_adjusted = pd.concat(country_chunk_data)

            del store_regions_adjusted["country"]
            del store_regions_adjusted[region_type]
            del store_regions_adjusted["countryID"]
        store_regions_adjusted.rename(columns={"store": "name"}, inplace=True)
        store_regions_adjusted["companyID"] = company.ids

        stores = Stores(self.db, self.insertion_mode)
        stores.write_to_db_multi_row(store_regions_adjusted, save_ids=True, show_progress_bar=False)
        return stores

    def write_categories(self, company: Company, categories_dict: t.Dict, categories_level_description: pd.DataFrame) -> t.Any:

        """Create and write a dummy product category.

        Args:
            company (Company): Company object.

        Returns:
            DummyCategory: The created dummy category.
        """

        categories_level_description = clean_and_check_categories_level_description(categories_level_description, copy=True)
        categories_dict = clean_and_check_categories_dict(categories_dict, copy=True)


        categories_level_description["companyID"] = company.ids
        categories_level_description.sort_values(by="level", inplace=True, ascending=True)

        # Set-up tables
        categoryleveldescriptions = CategoryLevelDescriptions(self.db, self.insertion_mode)
        categoryrelations = CategoryRelations(self.db, self.insertion_mode)
        categories = Categories(self.db, self.insertion_mode)

        # Write category level descriptions
        categoryleveldescriptions.write_to_db_multi_row(categories_level_description, save_ids=True)
        logger.info(f"Successfully wrote {len(categories_level_description)} category level descriptions")

        # Write categories by level
        for idx, row in categories_level_description.iterrows():
            level = row["level"]
            level_name = row["name"]

            relevant_cartegories = categories_dict[level]

            # Write categories
            unique_categories_df = pd.DataFrame({"name": list(relevant_cartegories.keys()), "companyID": company.ids})
            categories.write_to_db_multi_row(unique_categories_df, save_ids=True)
            
            # Write category relations
            category_relations_df = convert_to_df(relevant_cartegories)

            sub_categories = list(category_relations_df["subCategory"])
            sub_categories_unique = list(set(sub_categories))
            sub_category_ids_df = get_data_ids_by_company(self.db, company_id=company.ids, table_name = "categories", column_name="name", datapoints=sub_categories_unique)
            sub_category_ids_df.rename(columns={"ID": "subID"}, inplace=True)

            parent_categories = list(category_relations_df["parentCategory"])
            parent_categories_unique = list(set(parent_categories))
            parent_ids_df = get_data_ids_by_company(self.db, company_id=company.ids, table_name = "categories", column_name="name", datapoints=parent_categories_unique)
            parent_ids_df.rename(columns={"ID": "parentID"}, inplace=True)

            category_relations_df = category_relations_df.merge(sub_category_ids_df, left_on="subCategory", right_on="name", how="left")
            del category_relations_df["subCategory"]
            del category_relations_df["name"]
            category_relations_df = category_relations_df.merge(parent_ids_df, left_on="parentCategory", right_on="name", how="left")
            del category_relations_df["parentCategory"]
            del category_relations_df["name"]

            # highest level does not have parent ids
            if idx == 0:
                category_relations_df.dropna(inplace=True) 

            categoryrelations.write_to_db_multi_row(category_relations_df, save_ids=False)

            logger.info(f"Succesfully wrote level {level} categories ({level_name}) into the database")

        return categories

    def write_products(self, products: pd.DataFrame, company: Company) -> t.Any:
        
        """Create and write product entries.
        """

        products = clean_and_check_products(products, copy=True)

        company_id = company.ids

        unique_products = products["product"].unique()
        unique_products_df = pd.DataFrame({"product": unique_products})
        unique_products_df.rename(columns={"product": "name"}, inplace=True)
        unique_products_df["companyID"] = company_id

        products_object = Products(self.db, self.insertion_mode)
        products_object.write_to_db_multi_row(unique_products_df, save_ids=True, show_progress_bar=True)

        ids = products_object.ids
        unique_products_df["productID"] = ids
        
        return products, unique_products_df
    
    def write_product_categories(self, products: pd.DataFrame, unique_products_df: pd.DataFrame, company_object: Company, category_object: Categories, product_object: Products) -> t.Any:
        
        """Link products to a category and write associations.
        """

        products = clean_and_check_products(products, copy=True)

        # merge product ids
        products_with_ids = products.merge(unique_products_df, left_on="product", right_on="name", how="left")

        category_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name = "categories", column_name="name", datapoints=products_with_ids["category"].unique(), output_column_name="category", output_column_ID="categoryID")

        products_with_ids_and_category_ids = products_with_ids.merge(category_ids_df, left_on="category", right_on="category", how="left")
        products_with_ids_and_category_ids = products_with_ids_and_category_ids[["productID", "categoryID"]]

        product_categories = ProductCategories(self.db, self.insertion_mode)
        product_categories.write_to_db_multi_row(products_with_ids_and_category_ids, save_ids=False, show_progress_bar=True)

        return product_categories
    
    def write_skus(self, time_sku_data: pd.DataFrame, store_object: Stores, product_object: Products, company_object: Company) -> t.Any:
        
        """Create and write SKU entries.
        """

        time_sku_data = clean_and_check_time_sku_data(time_sku_data, copy=True)
        unique_stores = time_sku_data["store"].unique().tolist()
        unique_products = time_sku_data["product"].unique().tolist()

        store_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name = "stores", column_name="name", datapoints=unique_stores, output_column_name="store", output_column_ID="storeID")
        product_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name = "products",  column_name="name", datapoints=unique_products, output_column_name="product", output_column_ID="productID")

        time_sku_data = time_sku_data.merge(store_ids_df, left_on="store", right_on="store", how="left")
        time_sku_data = time_sku_data.merge(product_ids_df, left_on="product", right_on="product", how="left")

        # get unique store product pairs
        unique_store_product_pairs = time_sku_data[["storeID", "productID"]].drop_duplicates()

        skus = SKUTable(self.db, self.insertion_mode)
        skus.write_to_db_multi_row(unique_store_product_pairs, save_ids=True, show_progress_bar=True)

        unique_store_product_pairs["skuID"] = skus.ids

        # merge sku ids back on time_sku_data
        time_sku_data = time_sku_data.merge(unique_store_product_pairs, on=["storeID", "productID"], how="left")

        del time_sku_data["store"]
        del time_sku_data["product"]
        del time_sku_data["storeID"]
        del time_sku_data["productID"]
        
        return skus, time_sku_data

        
    def write_datapoints(self, time_sku_data_with_sku_id: pd.DataFrame) -> t.Any:
        
        """Create and write datapoint entries (sku-time combinations)
        """

        unique_dates = time_sku_data_with_sku_id["date"].unique().tolist()
        unique_dates = [str(date.date()) for date in unique_dates]

        date_ids_df = get_data_ids(self.db, table_name="dates", column_name="date", datapoints=unique_dates, output_column_ID="dateID")
        date_ids_df["date"] = pd.to_datetime(date_ids_df["date"])
        
        time_sku_data_with_sku_id = time_sku_data_with_sku_id.merge(date_ids_df, left_on="date", right_on="date", how="left")
        
        del time_sku_data_with_sku_id["date"]

        datapoint_df = time_sku_data_with_sku_id[["skuID", "dateID"]]

        datapoints = DataPoints(self.db, self.insertion_mode)
        logger.info("Writing datapoints to the database")
        datapoints.write_to_db_multi_row(datapoint_df, save_ids=True, show_progress_bar=True)

        time_sku_data_with_datapoint_id = time_sku_data_with_sku_id
        time_sku_data_with_datapoint_id["datapointID"] = datapoints.ids
        del time_sku_data_with_datapoint_id["skuID"]
        del time_sku_data_with_datapoint_id["dateID"]

        return datapoints, time_sku_data_with_datapoint_id

    def write_time_sku_data(self, time_sku_data_with_datapoint_id: pd.DataFrame, create_new_time_sku_table: bool = True) -> t.Any:
        
        """Create and write time-sku data entries.
        """

        columns = time_sku_data_with_datapoint_id.columns
        columns_without_id = [col for col in columns if col != "datapointID"]

        for column in columns_without_id:
            time_sku_data_object = GENERIC_TIME_SKU_DATA(self.db, self.insertion_mode, column)
            handle_time_sku_table_creation(self.db, column, create_new_time_sku_table)
            data = time_sku_data_with_datapoint_id[["datapointID", column]].copy()

            if column != "sales":
                # remove missing values
                # get number of missing values:
                missing_values = data[column].isna().sum()
                logger.info(f"Removing {missing_values} missing values from {column}")

                data = data.dropna(subset=[column])
            
            data = data.rename(columns={column: "value"}).copy()
            logger.info(f"Writing {column} data to the database")
            time_sku_data_object.write_to_db_multi_row(data, save_ids=False, show_progress_bar=True)

        return time_sku_data_with_datapoint_id

    def write_flags(self, not_for_sales_flag: pd.DataFrame, not_available_flag: pd.DataFrame, company_object: Company) -> t.Tuple[Flags]:
            
        """Create and write flags.
        """
        not_for_sales_flag = clean_and_check_not_for_sales_flag(not_for_sales_flag, copy=True)
        not_for_sales_flag["name"] = "not_for_sale"
        not_available_flag = clean_and_check_not_available_flag(not_available_flag, copy=True)
        not_available_flag["name"] = "not_available"
        company_id = company_object.ids


        # concate the two flags
        columns = not_for_sales_flag.columns

        # Filter out empty DataFrames
        dfs = [flag for flag in [not_for_sales_flag, not_available_flag] if not flag.empty]

        if dfs:
            flags = pd.concat(dfs)
        else:
            # Even if empty, create a DataFrame with the correct columns
            flags = pd.DataFrame(columns=columns)

        # convert dates to string on daily granularity
        flags["date"] = pd.to_datetime(flags["date"]).dt.date
        
        
        flag_ids = []
        rows_to_remove = [] 
        logger.info("Retrieving datapoint IDs for flags ...")
        args = list(zip(
            flags["product"].values,
            flags["date"].astype(str).values,
            flags["store"].values,
            [company_id] * len(flags),
            [company_id] * len(flags)
        ))
        args = tuple(args)


        values_str = ",\n".join(str(arg) for arg in args)

        query = f"""
            SELECT dp."ID" AS datapointID, p.name AS product, d.date AS date, s.name AS store
            FROM public.datapoints dp
            JOIN public.dates d ON dp."dateID" = d."ID"
            JOIN public.sku_table sku ON dp."skuID" = sku."ID"
            JOIN public.products p ON sku."productID" = p."ID"
            JOIN public.stores s ON sku."storeID" = s."ID"
            WHERE (p.name, d.date, s.name, p."companyID", s."companyID") IN (
                {values_str}
            );
        """

        datapoint_ids = self.db.execute_query(query, fetchall=True)


        datapoint_ids = pd.DataFrame(datapoint_ids, columns=["datapointID", "product", "date", "store"])
        
        # merge the datapoint ids back to the flags
        flags = flags.merge(datapoint_ids, on=["product", "date", "store"], how="left")

        # check if all flags have a datapointID
        if flags["datapointID"].isna().sum() > 0:
            logger.warning(f"Could not find a datapoint for {flags['datapointID'].isna().sum()} flags, removing from flags ...")
            # for index, row in tqdm(flags.iterrows()):
            #     if pd.isna(row["datapointID"]):
            #         if row["name"] == "not_for_sale":
            #             raise ValueError(
            #                 f"Could not find a datapoint for not_for_sale flag:\n\n{row}\n\n"
            #                 "Note: 'not_available' flags that are for empty datapoints are removed from flags "
            #                 "as the missing datapointID already indicates missing flag. However, for all 'not_for_sale' flags, "
            #                 "a datapointID is required, e.g., by making an entry into sales with sales set to zero."
            #                 )
        else:
            logger.info("All flags have a datapointID")

        flags = flags.dropna()

        del flags["product"]
        del flags["store"]
        del flags["date"]

        flags_object = Flags(self.db, self.insertion_mode)
        flags_object.write_to_db_multi_row(flags, save_ids=False, show_progress_bar=True)

        return Flags
    
    # def write_flags(self, not_for_sales_flag: pd.DataFrame, not_available_flag: pd.DataFrame, company_object: Company) -> t.Tuple[Flags]:
        
    #     """
    #     Create and write flags.
    #     """
        
    #     not_for_sales_flag = clean_and_check_not_for_sales_flag(not_for_sales_flag, copy=True)
    #     not_for_sales_flag["name"] = "not_for_sale"
    #     not_available_flag = clean_and_check_not_available_flag(not_available_flag, copy=True)
    #     not_available_flag["name"] = "not_available"
    #     company_id = company_object.ids

    #     # concate the two flags
    #     columns = not_for_sales_flag.columns

    #     # Filter out empty DataFrames
    #     dfs = [flag for flag in [not_for_sales_flag, not_available_flag] if not flag.empty]

    #     if dfs:
    #         flags = pd.concat(dfs)
    #     else:
    #         # Even if empty, create a DataFrame with the correct columns
    #         flags = pd.DataFrame(columns=columns)

    #     # convert dates to string on daily granularity
    #     flags["date"] = pd.to_datetime(flags["date"]).dt.date

    #     query = f"""
    #         SELECT dp."ID" AS datapointID, p.name AS product, d.date AS date, s.name AS store
    #         FROM public.datapoints dp
    #         JOIN public.dates d ON dp."dateID" = d."ID"
    #         JOIN public.sku_table sku ON dp."skuID" = sku."ID"
    #         JOIN public.products p ON sku."productID" = p."ID"
    #         JOIN public.stores s ON sku."storeID" = s."ID"
    #         WHERE p.name = %s
    #         AND d.date = %s
    #         AND s.name = %s
    #         AND p."companyID" = %s
    #         AND s."companyID" = %s

    #     """

    #     flag_ids = []
    #     rows_to_remove = [] 
        
    #     logger.info("Retrieving datapoint IDs for flags ...")
    #     args = [(row["product"], str(row["date"]), row["store"], company_id, company_id) for _, row in flags.iterrows()]
    #     args = tuple(args)

    #     datapoint_ids = self.db.execute_multi_query(query, args, fetchall=True)

    #     # check if datapoint_ids are empty
    #     if datapoint_ids:
    #         datapoint_ids = datapoint_ids[0]

    #     # create pandas
    #     datapoint_ids = pd.DataFrame(datapoint_ids, columns=["datapointID", "product", "date", "store"])
        
    #     # merge the datapoint ids back to the flags
    #     flags = flags.merge(datapoint_ids, on=["product", "date", "store"], how="left")

    #     # check if all flags have a datapointID
    #     if flags["datapointID"].isna().sum() > 0:
    #         logger.warning(f"Could not find a datapoint for {flags['datapointID'].isna().sum()} flags, removing from flags ...")
    #         # for index, row in tqdm(flags.iterrows()):
    #         #     if pd.isna(row["datapointID"]):
    #         #         if row["name"] == "not_for_sale":
    #         #             raise ValueError(
    #         #                 f"Could not find a datapoint for not_for_sale flag:\n\n{row}\n\n"
    #         #                 "Note: 'not_available' flags that are for empty datapoints are removed from flags "
    #         #                 "as the missing datapointID already indicates missing flag. However, for all 'not_for_sale' flags, "
    #         #                 "a datapointID is required, e.g., by making an entry into sales with sales set to zero."
    #         #                 )

                            
    #     flags = flags.dropna()

    #     del flags["product"]
    #     del flags["store"]
    #     del flags["date"]

    #     flags_object = Flags(self.db, self.insertion_mode)
    #     flags_object.write_to_db_multi_row(flags, save_ids=False, show_progress_bar=True)

    #     return Flags


    
    #################################### Optional data #############################################

    def write_store_data(self, store_feature_description_map: pd.DataFrame, store_feature_map: pd.DataFrame, store_object: Stores, company_object: Company) -> t.Tuple[StoreFeatureDescription, StoreFeatures]:
        
        """
        Create and write static store features.
        
        """

        store_feature_description_map = clean_and_check_store_feature_description_map(store_feature_description_map, copy=True)
        store_feature_map = clean_and_check_store_feature_data(store_feature_map, copy=True)
        company_id = company_object.ids
        store_feature_description_map["companyID"] = company_id

        store_feature_description = StoreFeatureDescription(self.db, self.insertion_mode)
        store_features = StoreFeatures(self.db, self.insertion_mode)

        if len(store_feature_description_map) == 0:
            logger.warning("Did not receive any store features, skipping ...")
            return store_feature_description, store_features
        
        store_feature_description.write_to_db_multi_row(store_feature_description_map, save_ids=True)

        store_feature_description_map["sfID"] = store_feature_description.ids
        del store_feature_description_map["description"]
        del store_feature_description_map["companyID"]
        store_feature_description_map.rename(columns={"name": "feature"}, inplace=True)

        store_feature_map = store_feature_map.merge(store_feature_description_map, left_on="feature", right_on="feature", how="left")
        del store_feature_map["feature"]

        store_ids_df = get_data_ids_by_company(self.db, company_id=company_id, table_name="stores", column_name="name", datapoints=store_feature_map["store"].unique(), output_column_name="store", output_column_ID="storeID") 

        store_feature_map = store_feature_map.merge(store_ids_df, left_on="store", right_on="store", how="left")
        del store_feature_map["store"]

        store_features.write_to_db_multi_row(store_feature_map, save_ids=False, show_progress_bar=False)

        return store_feature_description, store_features
    
    def write_product_data(self, product_feature_description_map: pd.DataFrame, product_feature_map: pd.DataFrame, product_object: Stores, company_object: Company) -> t.Tuple[ProductFeatureDescription, ProductFeatures]:
        
        """Create and write static product features.
        """

        product_feature_description_map = clean_and_check_product_feature_description_map(product_feature_description_map, copy=True)
        product_feature_map = clean_and_check_product_feature_data(product_feature_map, copy=True)
        company_id = company_object.ids
        product_feature_description_map["companyID"] = company_id

        product_feature_description = ProductFeatureDescription(self.db, self.insertion_mode)
        product_features = ProductFeatures(self.db, self.insertion_mode)

        if len(product_feature_description_map) == 0:
            logger.warning("Did not receive any product features, skipping ...")
            return product_feature_description, product_features
        
        product_feature_description.write_to_db_multi_row(product_feature_description_map, save_ids=True)

        product_feature_description_map["pfID"] = product_feature_description.ids
        del product_feature_description_map["description"]
        del product_feature_description_map["companyID"]
        product_feature_description_map.rename(columns={"name": "feature"}, inplace=True)

        product_feature_map = product_feature_map.merge(product_feature_description_map, left_on="feature", right_on="feature", how="left")

        product_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name="products", column_name="name", datapoints=product_feature_map["product"].unique(), output_column_name="product", output_column_ID="productID")

        product_feature_map = product_feature_map.merge(product_ids_df, left_on="product", right_on="product", how="left")
        del product_feature_map["product"]
        del product_feature_map["feature"]

        product_features.write_to_db_multi_row(product_feature_map, save_ids=False, show_progress_bar=True)

        return product_feature_description, product_features
    
    def write_time_product_data(self, time_product_feature_description_map: pd.DataFrame, time_product_feature_map: pd.DataFrame, product_object: Products, company_object: Company) -> t.Tuple[TimeProductFeatureDescription, TimeProductFeatures]:
        
        """

        Create and write time-product features.
        
        """

        time_product_feature_description_map = clean_and_check_time_product_feature_description_map(time_product_feature_description_map, copy=True)
        time_product_feature_map = clean_and_check_time_product_feature_data(time_product_feature_map, copy=True)
        company_id = company_object.ids
        time_product_feature_description_map["companyID"] = company_id
    
        time_product_feature_description = TimeProductFeatureDescription(self.db, self.insertion_mode)
        time_product_features = TimeProductFeatures(self.db, self.insertion_mode)

        if len(time_product_feature_description_map) == 0:
            logger.warning("Did not receive any time-product features, skipping ...")
        
        else:
            time_product_feature_description.write_to_db_multi_row(time_product_feature_description_map, save_ids=True)

            time_product_feature_description_map["tpfID"] = time_product_feature_description.ids
            del time_product_feature_description_map["description"]
            del time_product_feature_description_map["companyID"]
            time_product_feature_description_map.rename(columns={"name": "feature"}, inplace=True)

            time_product_feature_map = time_product_feature_map.merge(time_product_feature_description_map, left_on="feature", right_on="feature", how="left")
            del time_product_feature_map["feature"]

            product_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name="products", column_name="name", datapoints=time_product_feature_map["product"].unique(), output_column_name="product", output_column_ID="productID")

            time_product_feature_map = time_product_feature_map.merge(product_ids_df, left_on="product", right_on="product", how="left")
            del time_product_feature_map["product"]

            unique_dates = time_product_feature_map["date"].unique().tolist()
            unique_dates = [str(date.date()) for date in unique_dates]

            date_ids_df = get_data_ids(self.db, table_name="dates", column_name="date", datapoints=unique_dates, output_column_ID="dateID")
            date_ids_df["date"] = pd.to_datetime(date_ids_df["date"])

            time_product_feature_map = time_product_feature_map.merge(date_ids_df, left_on="date", right_on="date", how="left")
            del time_product_feature_map["date"]

            time_product_features.write_to_db_multi_row(time_product_feature_map, save_ids=False, show_progress_bar=True)

        return time_product_feature_description, time_product_features
            
            
        
    def write_time_region_data(self, time_region_feature_description_map: pd.DataFrame, time_region_feature_map: pd.DataFrame, company_object: Company) -> t.Tuple[TimeRegionFeatureDescription, TimeRegionFeatures]:
        
        """Create and write time-region features.
        """

        time_region_feature_description_map = clean_and_check_time_region_feature_description_map(time_region_feature_description_map, copy=True)
        time_region_feature_map = clean_and_check_time_region_feature_data(time_region_feature_map, copy=True)
        company_id = company_object.ids
        time_region_feature_description_map["companyID"] = company_id

        time_region_feature_description = TimeRegionFeatureDescription(self.db, self.insertion_mode)
        time_region_features = TimeRegionFeatures(self.db, self.insertion_mode)

        if len(time_region_feature_description_map) == 0:
            logger.warning("Did not receive any time-region features, skipping ...")
            return time_region_feature_description, time_region_features
        
        time_region_feature_description.write_to_db_multi_row(time_region_feature_description_map, save_ids=True)

        countries = time_region_feature_map["country"].unique()



        if len(time_region_feature_map.columns) == 5:
            for column_name in time_region_feature_map.columns:
                if column_name in ["date", "country", "feature", "value"]:
                    continue
                region_type = column_name
            
            subsets = []
            for country in countries:
                country_data = time_region_feature_map[time_region_feature_map["country"] == country]
                country_id = retrieve_data(self.db, "regions", "ID", f"abbreviation='{country}' AND type='country'")
                time_region_feature_map_subset = time_region_feature_map[time_region_feature_map["country"] == country]
                if not country_id:
                    raise ValueError(f"Country {country} not found in the database. Ensure the General Data pipeline is executed first. See step 3 in: https://github.com/d3group/foundry-master/blob/main/documentation/new_db_set_up.md")
                else:
                    country_id = country_id[0][0]
                
                condition = f"""
                    "country" = '{country_id}'
                    AND
                    "abbreviation" IN ({", ".join([f"'{region}'" for region in country_data[region_type].unique()])})
                """
                region_ids = retrieve_data(self.db, "regions", ["ID", "abbreviation"], condition=condition)
                
                # convert to DataFrame
                region_ids_df = pd.DataFrame(region_ids, columns=["regionID", "abbreviation"])
                region_ids_df.rename(columns={"abbreviation": region_type}, inplace=True)

                time_region_feature_map_subset = time_region_feature_map_subset.merge(region_ids_df, left_on=region_type, right_on=region_type, how="left")
                subsets.append(time_region_feature_map_subset)

            time_region_feature_map = pd.concat(subsets)

            del time_region_feature_map["country"]
            del time_region_feature_map[region_type]

        else:
            unique_countries = time_region_feature_map["country"].unique()
            condition = f"""
                "abbreviation" IN ({", ".join([f"'{country}'" for country in unique_countries])})
                AND
                "type" = 'country'
            """
            country_ids = retrieve_data(self.db, "regions", ["ID", "abbreviation"], condition=condition)
            country_ids_df = pd.DataFrame(country_ids, columns=["countryID", "abbreviation"])
            country_ids_df.rename(columns={"abbreviation": "country"}, inplace=True)

            time_region_feature_map = time_region_feature_map.merge(country_ids_df, left_on="country", right_on="country", how="left")
            del time_region_feature_map["country"]
            # rename countryID to regionID
            time_region_feature_map.rename(columns={"countryID": "regionID"}, inplace=True)    
        
        unique_feature_names = time_region_feature_map["feature"].unique()

        feature_ids_df = get_data_ids_by_company(self.db, company_id=company_object.ids, table_name="time_region_features_description", column_name="name", datapoints=unique_feature_names, output_column_name="feature", output_column_ID="trfID")

        time_region_feature_map = time_region_feature_map.merge(feature_ids_df, left_on="feature", right_on="feature", how="left")
        del time_region_feature_map["feature"]

        unique_dates = time_region_feature_map["date"].unique().tolist()
        unique_dates = [str(date.date()) for date in unique_dates]

        date_ids_df = get_data_ids(self.db, table_name="dates", column_name="date", datapoints=unique_dates, output_column_ID="dateID")
        date_ids_df["date"] = pd.to_datetime(date_ids_df["date"])

        time_region_feature_map = time_region_feature_map.merge(date_ids_df, left_on="date", right_on="date", how="left")
        del time_region_feature_map["date"]
        
        time_region_features.write_to_db_multi_row(time_region_feature_map, save_ids=False, show_progress_bar=False)


        return time_region_feature_description, time_region_features
    
    def write_time_store_data(self, time_store_feature_description_map: pd.DataFrame, time_store_feature_map: pd.DataFrame, store_object: Stores, company_object: Company) -> t.Tuple[TimeStoreFeatureDescription, TimeStoreFeatures]:
        
        """Create and write time-store features.
        """

        time_store_feature_description_map = clean_and_check_time_store_feature_description_map(time_store_feature_description_map, copy=True)
        time_store_feature_map = clean_and_check_time_store_feature_data(time_store_feature_map, copy=True)
        company_id = company_object.ids
        time_store_feature_description_map["companyID"] = company_id

        time_store_feature_description = TimeStoreFeatureDescription(self.db, self.insertion_mode)
        time_store_features = TimeStoreFeatures(self.db, self.insertion_mode)

        if len(time_store_feature_description_map) == 0:
            logger.warning("Did not receive any time-store features, skipping ...")
            return time_store_feature_description, time_store_features

        time_store_feature_description.write_to_db_multi_row(time_store_feature_description_map, save_ids=True)

        time_store_feature_description_map["tsfID"] = time_store_feature_description.ids

        del time_store_feature_description_map["description"]
        del time_store_feature_description_map["companyID"]
        time_store_feature_description_map.rename(columns={"name": "feature"}, inplace=True)

        time_store_feature_map = time_store_feature_map.merge(time_store_feature_description_map, left_on="feature", right_on="feature", how="left")
        del time_store_feature_map["feature"]

        store_ids_df = get_data_ids_by_company(self.db, company_id=company_id, table_name="stores", column_name="name", datapoints=time_store_feature_map["store"].unique(), output_column_name="store", output_column_ID="storeID")

        time_store_feature_map = time_store_feature_map.merge(store_ids_df, left_on="store", right_on="store", how="left")
        del time_store_feature_map["store"]

        # get dates
        unique_dates = time_store_feature_map["date"].unique().tolist()
        unique_dates = [str(date.date()) for date in unique_dates]

        date_ids_df = get_data_ids(self.db, table_name="dates", column_name="date", datapoints=unique_dates, output_column_ID="dateID")
        date_ids_df["date"] = pd.to_datetime(date_ids_df["date"])
    
        time_store_feature_map = time_store_feature_map.merge(date_ids_df, left_on="date", right_on="date", how="left")
        del time_store_feature_map["date"]
        
        logger.info("Writing time-store features to the database")
        time_store_features.write_to_db_multi_row(time_store_feature_map, save_ids=False, show_progress_bar=True)

        return time_store_feature_description, time_store_features
    

