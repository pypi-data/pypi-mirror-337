from pathlib import Path
from tempfile import TemporaryDirectory

from moto import mock_s3


@mock_s3
def test_bucket_put(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_file_exists(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    success = bucket.check_file_exists("text.txt")
    assert success is True

    file_text = "test"
    response = bucket.put("subdir/text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    success = bucket.check_file_exists("subdir/text.txt")
    assert success is True

    success = bucket.check_file_exists("doesnotexist/text.txt")
    assert success is False


@mock_s3
def test_bucket_get(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    data, metadata = bucket.get("text.txt")
    assert data == b"test"


@mock_s3
def test_bucket_get_decode(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    data, metadata = bucket.get("text.txt", decode=True)
    assert data == "test"


@mock_s3
def test_bucket_delete(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    response = bucket.delete_file("text.txt")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 204


@mock_s3
def test_bucket_upload(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as upload:
        success = bucket.upload_file(upload.name, upload.name)

    assert success is True


@mock_s3
def test_bucket_download(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as upload:
        success = bucket.upload_file(upload.name, upload.name)

    assert success is True

    with create_tempfile("txt") as download:
        success = bucket.download_file(upload.name, download.name)
        assert success is True

        with open(download.name, encoding="UTF-8") as f:
            assert f.read() == "test"


@mock_s3
def test_bucket_transfer(bucket, bucket2, create_tempfile):
    bucket.create()
    bucket2.create()

    with create_tempfile("txt") as upload:
        filename = upload.name
        key = filename.lstrip("/")

        success = bucket.upload_file(key, filename)
        assert success is True

    success = bucket.transfer(key, "testing2", f"newkey/{key}")
    assert success is True

    exists = bucket2.check_file_exists(f"newkey/{key}")
    assert exists is True


@mock_s3
def test_bucket_transfer_exists(bucket, bucket2, create_tempfile):
    bucket.create()
    bucket2.create()

    with create_tempfile("txt") as upload:
        filename = upload.name

        success = bucket.upload_file(upload.name, upload.name)
        assert success is True

        success = bucket2.upload_file(upload.name, upload.name)
        assert success is True

    success = bucket.transfer(filename, "testing2", filename)
    assert success is True


@mock_s3
def test_list_all(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.txt"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_all()
    assert len(file_list) == 3


@mock_s3
def test_list_dir_root(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir()
    assert len(file_list) == 1


@mock_s3
def test_list_dir_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True)
    assert len(file_list) == 3


@mock_s3
def test_list_dir_ext_no_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(file_type="csv")

    assert file_list == []


@mock_s3
def test_list_dir_ext_recursive(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True, file_type="csv")

    assert len(file_list) == 1
    assert file_list[0] == "dir1/dir2/test.csv"


@mock_s3
def test_list_dir_ext_recursive_names_only(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/dir2/test2.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(recursive=True, file_type="csv", names_only=True)

    assert len(file_list) == 1
    assert file_list[0] == "test2"


@mock_s3
def test_list_dir_ext_path(bucket):
    bucket.create()

    file_names = ["test.txt", "dir1/test.txt", "dir1/test.csv", "dir1/dir2/test.csv"]
    for file_name in file_names:
        response = bucket.put(file_name, "test")
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    file_list = bucket.list_dir(path="dir1", file_type="csv")

    assert len(file_list) == 1
    assert file_list[0] == "dir1/test.csv"


@mock_s3
def test_upload_dir(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        temp1 = create_tempfile("txt", temp_dir=temp_dir, delete=False)
        temp2 = create_tempfile("txt", temp_dir=temp_dir, delete=False)
        temp3 = create_tempfile("csv", temp_dir=temp_dir, delete=False)

        temp_subdir = TemporaryDirectory(dir=temp_dir)
        temp4 = create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)
        temp5 = create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir(temp_dir)

    name_list = [f.name for f in [temp1, temp2, temp3, temp4, temp5]]
    for name in name_list:
        assert status_dict[name] is True
        exists = bucket.check_file_exists(name.split("/tmp/")[1])
        assert exists


@mock_s3
def test_upload_dir_contents_only(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir1:
        with TemporaryDirectory(dir=temp_dir1) as temp_dir2:
            with TemporaryDirectory(dir=temp_dir2) as temp_dir3:
                with TemporaryDirectory(dir=temp_dir3) as temp_dir4:

                    temp1 = create_tempfile("txt", temp_dir=temp_dir4, delete=False)
                    temp2 = create_tempfile("txt", temp_dir=temp_dir4, delete=False)
                    temp3 = create_tempfile("csv", temp_dir=temp_dir4, delete=False)

                    temp_subdir = TemporaryDirectory(dir=temp_dir4)
                    temp4 = create_tempfile(
                        "txt", temp_dir=temp_subdir.name, delete=False
                    )
                    temp5 = create_tempfile(
                        "txt", temp_dir=temp_subdir.name, delete=False
                    )

                    temp_subdir2 = TemporaryDirectory(dir=temp_dir4)
                    temp6 = create_tempfile(
                        "txt", temp_dir=temp_subdir2.name, delete=False
                    )

                    temp_subdir3 = TemporaryDirectory(dir=temp_subdir2.name)
                    temp7 = create_tempfile(
                        "txt", temp_dir=temp_subdir3.name, delete=False
                    )

                    status_dict = bucket.upload_dir(temp_dir4, contents_only=True)

    name_list = [f.name for f in [temp1, temp2, temp3, temp4, temp5, temp6, temp7]]
    for name in name_list:
        assert status_dict[name] is True
        exists = bucket.check_file_exists(name.split(temp_dir4)[1])
        assert exists


@mock_s3
def test_upload_dir_with_file_type(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        csv = create_tempfile("csv", temp_dir=temp_dir, delete=False)

        temp_subdir = TemporaryDirectory(dir=temp_dir)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir(temp_dir, s3_path="/testing", file_type="csv")

    assert status_dict[csv.name] is True
    csv_key = "testing/" + csv.name.split("/tmp/")[1]
    exists = bucket.check_file_exists(csv_key)
    assert exists


@mock_s3
def test_download_all(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as upload_dir:

        temp1 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        temp2 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        temp3 = create_tempfile("csv", temp_dir=upload_dir, delete=False)

        upload_subdir = TemporaryDirectory(dir=upload_dir)
        temp4 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)
        temp5 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)

        status_dict = bucket.upload_dir(upload_dir)

    name_list = [f.name for f in [temp1, temp2, temp3, temp4, temp5]]
    for name in name_list:
        assert status_dict[name] is True
        exists = bucket.check_file_exists(name.split("/tmp/")[1])
        assert exists

    with TemporaryDirectory() as download_dir:

        status_dict = bucket.download_all(download_dir)

        for file in Path(download_dir).glob("**/*"):
            if file.is_file():
                with open(file, encoding="UTF-8") as f:
                    assert f.read() == "test"

    for name in name_list:
        key = Path(*Path(name).parts[2:])
        assert status_dict[str(key)] is True


@mock_s3
def test_download_dir_with_file_type(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as upload_dir:

        txt1 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        txt2 = create_tempfile("txt", temp_dir=upload_dir, delete=False)
        csv = create_tempfile("csv", temp_dir=upload_dir, delete=False)

        upload_subdir = TemporaryDirectory(dir=upload_dir)
        txt3 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)
        txt4 = create_tempfile("txt", temp_dir=upload_subdir.name, delete=False)

        status_dict = bucket.upload_dir(upload_dir, s3_path="/testing")

    name_list = [f.name for f in [txt1, txt2, csv, txt3, txt4]]
    for name in name_list:
        assert status_dict[name] is True

    with TemporaryDirectory() as download_dir:

        status_dict = bucket.download_dir("/testing", download_dir, file_type="csv")

        for file in Path(download_dir).glob("**/*"):
            if file.is_file():
                with open(file, encoding="UTF-8") as f:
                    assert f.read() == "test"

    key = "testing" / Path(*Path(csv.name).parts[2:])
    assert status_dict[str(key)] is True


@mock_s3
def test_delete_dir(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        temp1 = create_tempfile("txt", temp_dir=temp_dir, delete=False)
        temp_subdir = TemporaryDirectory(dir=temp_dir)
        temp2 = create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir(temp_dir)

    name_list = [f.name for f in [temp1, temp2]]
    for name in name_list:
        assert status_dict[name] is True

        s3_key = name.split("/tmp/")[1]
        exists = bucket.check_file_exists(s3_key)
        assert exists

    status_dict = bucket.delete_dir(temp_subdir.name.split("/tmp/")[1])
    assert status_dict[temp2.name.split("/tmp/")[1]] is True


@mock_s3
def test_delete_dir_with_file_type(bucket, create_tempfile):
    bucket.create()

    with TemporaryDirectory() as temp_dir:

        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        create_tempfile("txt", temp_dir=temp_dir, delete=False)
        csv = create_tempfile("csv", temp_dir=temp_dir, delete=False)

        temp_subdir = TemporaryDirectory(dir=temp_dir)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)
        create_tempfile("txt", temp_dir=temp_subdir.name, delete=False)

        status_dict = bucket.upload_dir(temp_dir, s3_path="/testing")

    assert status_dict[csv.name] is True
    csv_key = "testing/" + csv.name.split("/tmp/")[1]
    exists = bucket.check_file_exists(csv_key)
    assert exists

    status_dict = bucket.delete_dir("testing", file_type="csv")
    assert status_dict[csv_key] is True
    exists = bucket.check_file_exists(csv_key)
    assert not exists


@mock_s3
def test_rename_file(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    success = bucket.rename_file("text.txt", "text_renamed.txt")
    assert success is True

    success = bucket.check_file_exists("text.txt")
    assert success is False

    success = bucket.check_file_exists("text_renamed.txt")
    assert success is True
