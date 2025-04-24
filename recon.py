"""
This file will be used to do the reconciliation between Postgres and Milvus.
"""
from pymilvus import (Collection, connections)
import sys
import psycopg2 as pg
import pandas as pd
import streamlit as st


def query_postgres(project_id, corpus_type):
    conn = None

    try:

        # Connecting to PostgreSQL cluster.
        conn = pg.connect(
            host="localhost",
            database="talktocorpusdb",
            user=st.secrets.RECONCILIATION.postgres_user,
            password=st.secrets.RECONCILIATION.postgres_password,
            port=5430
        )
        conn.autocommit = True
        print("connected to postgres..")
        # Creating a Cursor
        review_cursor = conn.cursor()
        # The connecting schema, where the table resides
        review_cursor.execute("SET search_path='corpus'")
        # Now building the query text.
        # You can play with the query.
        sql_text = "select c.fileid fileid, i.filename filename,  count(*) cnt " \
                   "FROM CORPUS.corpusdetail c, " \
                   "(SELECT DISTINCT originalfileid, filename, PROJECTID " \
                   " FROM CORPUS.ingestionsummary " \
                   " WHERE PROJECTID= %(project_id)s ) i " \
                   "WHERE c.PROJECTID= %(project_id)s " \
                   "AND c.STATUS='active' " \
                   "AND c.CORPUS_TYPE in %(corpus_type)s   " \
                   "AND REF_SECTION_ID IS NOT NULL " \
                   "AND c.PROJECTID=i.PROJECTID AND c.fileid=i.originalfileid " \
                   "GROUP BY c.fileid, i.filename ORDER BY fileid "
        params = {'project_id': project_id, 'corpus_type': corpus_type}
        review_cursor.mogrify(sql_text, params)
        # Executing the cursor
        review_cursor.execute(sql_text, params)
        sql_result = review_cursor.fetchall()
        conn.close()
        # Return the result set as pandas data frame
        df = pd.DataFrame(sql_result, columns=['file_id', 'postgres_file_name', 'postgres_count'])
        return df
    except Exception as e:
        print("Error in query_postgres")
        print(e)
    finally:
        if conn is not None:
            conn.close()


def query_milvus(collection_name, file_id_list):
    try:
        # Connect to secure Milvus.
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user=st.secrets.RECONCILIATION.milvus_user,
                            password=st.secrets.RECONCILIATION.milvus_password,
                            secure=True,
                            client_key_path='.\\Certs\\prodtls.key',
                            client_pem_path='.\\Certs\\prodtls.crt',
                            ca_pem_path='.\\Certs\\prodtls.crt',
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)

    try:
        # Pass the collection name for query
        collection = Collection(collection_name)
        df1 = pd.DataFrame(columns=['file_id', 'milvus_count'])
        i = 0

        # Try to improve this with batch select.
        for fileid in file_id_list:
            expr_qry = 'fileid == "' + fileid + '"'
            res = collection.query(expr=expr_qry, output_fields=["count(*)"])
            df1.loc[i] = [fileid, res[0]["count(*)"]]
            i = i + 1
        return df1
    except Exception as e:
        print("Problem in query_milvus")
        print(e)
    finally:
        if connections is not None:
            connections.disconnect("default")


def find_unique_file_ids_milvus(collection_name):
    try:
        # Connect to secure Milvus.
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user=st.secrets.RECONCILIATION.milvus_user,
                            password=st.secrets.RECONCILIATION.milvus_password,
                            secure=True,
                            client_key_path='.\\Certs\\prodtls.key',
                            client_pem_path='.\\Certs\\prodtls.crt',
                            ca_pem_path='.\\Certs\\prodtls.crt',
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)

    try:
        # Pass the collection name for query
        collection = Collection(collection_name)
        df1 = pd.DataFrame(columns=['file_id', 'milvus_file_name'])
        i = 0
        # You can play with the batch size to find optimum size.
        batch_size = 1000
        query_iterator = collection.query_iterator(batch_size, expr="",
                                                   output_fields=["fileid", "filename"])

        while True:
            # turn to the next page
            res = query_iterator.next()
            if len(res) == 0:
                print("query iteration finished, close")
                # close the iterator
                query_iterator.close()
                break
            for j in range(len(res)):
                df1.loc[i] = [res[j]["fileid"], res[j]["filename"]]
                i = i + 1
        # Removing the duplicates.
        df1.drop_duplicates(subset=['file_id'], keep='last', inplace=True)
        return df1
    except Exception as e:
        print("Problem in find_unique_file_ids_milvus")
        print(e)
    finally:
        if connections is not None:
            connections.disconnect("default")


def query_milvus_iterator(collection_name, file_id_list):
    # This function is not ready yet, can add some performance benefit
    # if implemented, but it is challenging as Milvus doesn't have grouping search in scalar field.

    try:
        # Connect to secure Milvus.
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user=st.secrets.RECONCILIATION.milvus_user,
                            password=st.secrets.RECONCILIATION.milvus_password,
                            secure=True,
                            client_key_path='.\\Certs\\prodtls.key',
                            client_pem_path='.\\Certs\\prodtls.crt',
                            ca_pem_path='.\\Certs\\prodtls.crt',
                            show_startup_banner=True
                            )
        print("Connected to Milvus")
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)

    try:
        # Pass the collection name for query
        collection = Collection(collection_name)
        df1 = pd.DataFrame(columns=['file_id', 'milvus_count'])
        i = 0
        # build query expression
        expr = "fileid in ["
        for fid in file_id_list:
            expr = expr + '"' + str(fid) + '" ,'
        expr = expr + "]"
        print(expr)

        # You can play with the batch size to find optimum size.
        batch_size = 1000
        query_iterator = collection.query_iterator(batch_size, expr=expr,
                                                   output_fields=["fileid", "count(*)"])
        while True:
            # turn to the next page
            res = query_iterator.next()
            if len(res) == 0:
                print("query iteration finished, close")
                # close the iterator
                query_iterator.close()
                break
            for j in range(len(res)):
                print(res[j])
                df1.loc[i] = [res[j]["fileid"], res[j]["count(*)"]]
                i = i + 1
        return df1
    except Exception as e:
        print("Problem in query_milvus")
        print(e)
    finally:
        if connections is not None:
            connections.disconnect("default")


if __name__ == '__main__':
    # reconciliation between postgres and milvus
    # The below variable is a tuple, if you want to pass only one value then also
    # you need to keep it ad tuple e.g. ('document',)
    v_corpus_type = ('document', 'feedback', 'knowledge_articles', 'service_catalog')
    v_project_id = 'MAPFREBR'
    v_collection_name = 'MAPFREBR'

    pg_result = query_postgres(v_project_id, v_corpus_type)
    print("The number of unique file ids in Postgres: ", pg_result.shape[0])

    milvus_file_ids = find_unique_file_ids_milvus(v_collection_name)
    file_ids = milvus_file_ids['file_id'].tolist()
    print("The number of unique file ids in Milvus: ", milvus_file_ids.shape[0])
    milvus_result = query_milvus(v_collection_name, file_ids)
    milvus_result_filename = pd.merge(milvus_file_ids, milvus_result, on='file_id', how='inner')
    print("The number of unique file ids with name in Milvus: ", milvus_result_filename.shape[0])
    merged_result = pd.merge(pg_result, milvus_result_filename, on='file_id', how='outer')
    conditions = merged_result["postgres_count"] == merged_result["milvus_count"]
    merged_result["matched"] = 0
    merged_result.loc[conditions, "matched"] = 1
    merged_result.to_csv("recon_total.csv", index=False)
    print("Mismatched file Ids")
    print("*" * 40)
    mismatched_results = merged_result[merged_result["matched"] == 0]
    print(mismatched_results.to_string(index=False))
    mismatched_results.to_csv("recon.csv", index=False)
