import pytest
import os

############# DYNAMIC PARAMETRIZATION #############
def pytest_generate_tests(metafunc):
    listing = os.listdir() # directory of csv files
    csv_files = [item for item in listing if item.endswith('.csv')]

    # Dynamiczne przypisanie wszystkim fixtures i funkcjom testowym zależnym od csv_file listę parametrów w postaci listy nazw plików csv
    if 'csv_file' in metafunc.fixturenames:
        metafunc.parametrize('csv_file', csv_files)

############# FIXTURES #############

############# STATIC PARAMETRIZATION #############
# @pytest.fixture(params = ['address.csv', 'book.csv', 'customer.csv'])
# def csv_data(request):
#     with open(request.param) as f:
#         data = f.read().split('\n')
#     return data

############# DYNAMIC PARAMETRIZATION #############
@pytest.fixture()
def csv_data(csv_file):
    with open(csv_file) as f:
        data = f.read().split('\n')
    return data


@pytest.fixture()
def csv_header(csv_data):
    return csv_data[0]


@pytest.fixture()
def csv_records(csv_data):
    return csv_data[1:]


@pytest.fixture()
def column_names(csv_header):
    return csv_header.split(',')


############# TESTS #############
def test_header_is_uppercase(csv_header):
    """Check if column names in header are uppercase"""
    assert csv_header == csv_header.upper()


def test_header_starts_with_id(column_names):
    """Check if the first column in header is ID"""
    assert column_names[0] == 'ID'


############# STATIC PARAMETRIZATION OF FUNCTIONS #############
@pytest.mark.parametrize('checked_name', ['CREATED', 'UPDATED'])
def test_header_has_column(column_names, checked_name):
    """Check if header has column CREATED and UPDATED"""
    assert checked_name in column_names

# def test_header_has_column_created(column_names):
#     """Check if header has column CREATED"""
#     assert "CREATED" in column_names


# def test_header_has_column_updated(column_names):
#     """Check if header has column UPDATED"""
#     assert "UPDATED" in column_names


def test_record_matches_header(column_names, csv_records):
    """Check if number of columns in each record matches header"""
    num_of_columns = len(column_names)
    errors = []
    for record in csv_records:
        if len(record.split(',')) != num_of_columns:
            errors.append(record) #assert False
    assert not errors


def test_record_first_field_is_number(csv_records):
    """Check if the first value in each record is a number"""
    errors = []
    for record in csv_records:
        record_splitted = record.split(',')
        if not record_splitted[0].isdigit():
            errors.append(record)
    assert not errors