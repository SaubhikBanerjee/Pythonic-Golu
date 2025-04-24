"""
This file will be used to delete from Milvus.
"""
from pymilvus import (Collection, connections)
import sys
import pandas as pd
import streamlit as st


def find_pk_ids_milvus(collection_name, fileid_list):
    try:
        # Connect to secure Milvus.
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user=st.secrets.UAT.milvus_user,
                            password=st.secrets.UAT.milvus_password,
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
        df1 = pd.DataFrame(columns=['id_pk'])
        i = 0
        # You can play with the batch size to find optimum size.
        batch_size = 500
        modified_fileid = ""
        print("preparing query expr")
        for item in fileid_list:
            if modified_fileid != "":
                modified_fileid = modified_fileid + ",'" + str(item) + "'"
            else:
                modified_fileid = "'" + str(item) + "'"
        expr_qry = "fileid in [" + modified_fileid + "]"
        print("building query expr complete")
        query_iterator = collection.query_iterator(batch_size, expr=expr_qry,
                                                   output_fields=["pk"])
        print("Query iterator started")
        while True:
            # turn to the next page
            res = query_iterator.next()
            if len(res) == 0:
                print("query iteration finished, close")
                # close the iterator
                query_iterator.close()
                break
            for j in range(len(res)):
                df1.loc[i] = [res[j]["id"]]
                i = i + 1

        return df1
    except Exception as e:
        print("Problem in find_pk_ids_milvus")
        print("Error:", e)
    finally:
        if connections is not None:
            connections.disconnect("default")


def delete_record_milvus(collection_name, input_pk_list):
    try:
        # Connect to secure Milvus.
        connections.connect("default",
                            host="localhost",
                            server_name="localhost",
                            port=19530,
                            user=st.secrets.UAT.milvus_user,
                            password=st.secrets.UAT.milvus_password,
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
        print("preparing query expr")
        modified_pk_list = ""
        for item in input_pk_list:
            if modified_pk_list != "":
                modified_pk_list = modified_pk_list + ",'" + str(item) + "'"
            else:
                modified_pk_list = "'" + str(item) + "'"
        expr_qry = "id in [" + modified_pk_list + "]"
        print("building query expr for delete complete")
        collection.delete(expr_qry)
        print("Deletion done")
    except Exception as e:
        print("Problem in delete_record_milvus")
        print("Error:", e)
    finally:
        if connections is not None:
            connections.disconnect("default")


if __name__ == '__main__':
    df = pd.read_csv("data-1745487387983.csv")
    print(df.head())
    print("The number of file_id: ", df.shape[0])
    file_id = df["fileid"].tolist()
    v_collection_name = 'Hubbell'
    print("Calling find_pk_ids_milvus")
    df_pk = find_pk_ids_milvus(v_collection_name, file_id)
    print(df_pk.head())
    print("The number of pk in Milvus: ", df_pk.shape[0])
    pk_list = df_pk["id_pk"].tolist()
    delete_record_milvus(v_collection_name, pk_list)
