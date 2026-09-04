from typing import Dict

import time
import requests
from pandas import DataFrame, read_csv, read_json, to_datetime

def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """Get the public holidays for the given year for Brazil.

    Args:
        public_holidays_url (str): url to the public holidays.
        year (str): The year to get the public holidays for.

    Raises:
        SystemExit: If the request fails.

    Returns:
        DataFrame: A dataframe with the public holidays.
    """
    # TODO: Implement this function.
    # You must use the requests library to get the public holidays for the given year.
    # The url is public_holidays_url/{year}/BR.
    # You must delete the columns "types" and "counties" from the dataframe.
    # You must convert the "date" column to datetime.
    # You must raise a SystemExit if the request fails. Research the raise_for_status
    # method from the requests library.
    url = f"{public_holidays_url}/{year}/BR"

    max_attempts = 5

    base_delay = 1

    max_delay = 30

    for attempt in range(max_attempts):

        try:

            response = requests.get(url, timeout=10)

            response.raise_for_status()

            break

        except requests.exceptions.Timeout:

            if attempt == max_attempts - 1:

                raise SystemExit("Request timed out after multiple attempts")

            # Exponential backoff capped at max_delay

            delay = min(base_delay * (2 ** attempt), max_delay)

            print(f"Request timed out. Retrying in {delay} seconds...")

            time.sleep(delay)

        except requests.exceptions.RequestException as exc:

            raise SystemExit(f"Failed to retrieve public holidays: {exc}")

    holidays = DataFrame(response.json())

    holidays = holidays.drop(columns=["types", "counties"])
    holidays["date"] = to_datetime(holidays["date"])

    return holidays

def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes
