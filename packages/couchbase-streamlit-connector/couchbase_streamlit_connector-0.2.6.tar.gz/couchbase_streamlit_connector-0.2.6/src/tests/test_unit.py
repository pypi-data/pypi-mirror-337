from couchbase_streamlit_connector.connector import CouchbaseConnector
import streamlit as st
import pytest
from unittest.mock import MagicMock, patch
     
@pytest.fixture
@patch('couchbase_streamlit_connector.connector.Cluster')
def connection(mock_Cluster):
    
    mock_collection_object = MagicMock()    
    # for test_create
    mock_collection_object.insert.return_value = "mock_insert_result"
    # for test_read
    mock_get_result = MagicMock()
    mock_get_result.content_as = {dict: "mock_get_result"}
    mock_collection_object.get.return_value = mock_get_result
    # for test_update
    mock_collection_object.replace.return_value = "mock_replace_result"
    # for test_delete
    mock_collection_object.remove.return_value = "mock_remove_result"
    
    mock_scope_object = MagicMock()
    mock_scope_object.collection.return_value = mock_collection_object
    
    mock_bucket_object = MagicMock()
    mock_bucket_object.scope.return_value = mock_scope_object
    
    mock_cluster_object = MagicMock()
    mock_cluster_object.bucket.return_value = mock_bucket_object
    mock_cluster_object.wait_until_ready.return_value = True
    # for test_query
    mock_cluster_object.query.return_value = "mock_query_result"

    mock_Cluster.return_value = mock_cluster_object
    
    connection = st.connection(
        "couchbase", 
        type=CouchbaseConnector, 
        CONNSTR= "CONNSTR",
        USERNAME= "USERNAME",
        PASSWORD= "PASSWORD",
        BUCKET_NAME= "BUCKET_NAME",
        SCOPE_NAME= "SCOPE_NAME",
        COLLECTION_NAME= "COLLECTION_NAME"
    )
    
    return connection
    
def test_create(connection):
    """Test the successful creation of an airline"""
    assert connection.insert_document("doc1", {"name": "Alice"}) == "mock_insert_result"
            
def test_read(connection):
    """Test the reading of an airline"""
    assert connection.get_document("doc1") == "mock_get_result"
    
def test_update(connection):
    """Test updating an existing airline"""
    assert connection.replace_document("doc1", {"name": "Alice", "age": 25}) == "mock_replace_result"
    
def test_delete(connection):
    """Test deleting an existing airline"""
    assert connection.remove_document("doc1") == "mock_remove_result"
    
def test_query(connection):
    """Test the destination airports from an airline""
    # query = """
    assert connection.query("SELECT * FROM `test`") == "mock_query_result"

def test_set_bucket_scope_coll(connection):
    """Test setting bucket, scope, and collection"""
    connection.set_bucket_scope_coll("test_bucket", "test_scope", "test_collection")

    assert connection.bucket_name == "test_bucket"
    assert connection.scope_name == "test_scope"
    assert connection.collection_name == "test_collection"
    assert connection.bucket is not None
    assert connection.scope is not None
    assert connection.collection is not None
    
def test_get_bucket_scope_coll(connection):
    """Test getting bucket, scope, and collection"""
    connection.bucket_name = "test_bucket"
    connection.scope_name = "test_scope"
    connection.collection_name = "test_collection"
    connection.bucket = MagicMock()
    connection.scope = MagicMock()
    connection.collection = MagicMock()
    
    returnde_obj = connection.get_bucket_scope_coll()
    
    assert returnde_obj['bucket_name'] == "test_bucket"
    assert returnde_obj['scope_name'] == "test_scope"
    assert returnde_obj['collection_name'] == "test_collection"
    assert returnde_obj['bucket'] is not None
    assert returnde_obj['scope'] is not None
    assert returnde_obj['collection'] is not None