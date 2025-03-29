from io import BytesIO
import json
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import requests


class VoltusClient:
    """
    A client for interacting with the Voltus feature store API.

    Attributes:
        api_url (str): The base URL of the Voltus API.
        token (str): The authentication token.
    """

    def __init__(self, api_base_url: str, token: str, verify_requests: bool = True):
        """
        Initializes the VoltusClient.

        Args:
            api_url: The base URL of the Voltus API.
        """
        # checking inputs
        if api_base_url is None:
            raise Exception(f"'api_base_url' is required. Got '{api_base_url}'")
        elif not isinstance(api_base_url, str):
            raise Exception(
                f"'api_base_url' must be a string. Got {type(api_base_url)}"
            )

        if token is None:
            raise Exception(f"'token' is required. Got '{token}'")
        elif not isinstance(token, str):
            raise Exception(f"'token' must be a string. Got {type(token)}")

        # parsing api_base_url
        self.url = (
            api_base_url.replace("\\", "/")
            .replace("https://", "")
            .replace("http://", "")
            .strip("/")
            .strip()
        )
        self.token = token
        self.verify_requests = verify_requests
        self.healthcheck()

        # Get example dataset names
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/examples/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to get example datasets. response status code: {response.status_code}, text: {response.text}"
            )
        example_dataset_names = response.json()
        if not isinstance(example_dataset_names, list):
            raise Exception(
                f"Failed to get example datasets: Response is not a list. response status code: {response.status_code}, text: {response.text}"
            )
        if len(example_dataset_names) == 0:
            raise Exception(
                f"Failed to get example datasets: Returned list is empty. response status code: {response.status_code}, text: {response.text}"
            )
        print("Example dataset names:", example_dataset_names)
        self.example_dataset_names = example_dataset_names

    def healthcheck(self) -> bool:
        try:
            response = requests.get(
                verify=self.verify_requests,
                url=f"https://{self.url}/v1/current_authenticated_user",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "accept": "application/json",
                },
            )
        except requests.exceptions.ConnectionError:
            raise Exception(f"Failed to connect to '{self.url}'.")

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(
                f"Healthcheck failed when creating client. response status code: {response.status_code}, text: {response.text}"
            )

        response_json = response.json()
        if "user" not in response_json.keys():
            raise Exception(
                f"Healthcheck failed when creating client: user not in response.json(). response: {response_json}"
            )

        if response_json["user"] is None:
            raise Exception(
                f"Healthcheck failed when creating client: user is None. response: {response_json}"
            )

        if "token" not in response_json["user"].keys():
            raise Exception(
                f"Healthcheck failed when creating client: token not in response_json['user']. response: {response_json}"
            )

        if response_json["user"]["token"].split(".")[0] != self.token.split(".")[0]:
            raise Exception(
                f"Healthcheck failed when creating client: token mismatch. response: {response_json}\nself.token: {self.token}\nresponse_json['user']['token']: {response_json['user']['token']}"
            )

        return True

    def get_task_status(self, task_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Gets the status of an asynchronous task.

        Args:
            task_id (Optional[str], optional): The ID of the task. If None, retrieves the status of all tasks. Defaults to None.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing the status of a task.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/task_status",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={"task_id": task_id},
        )
        return response.json()

    def get_current_authenticated_user(self):
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/current_authenticated_user",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )
        return response.json()

    def upload_dataset(
        self,
        dataset: pd.DataFrame,
        dataset_name: str = "new dataset",
        description: str = "",
        overwrite: bool = True,
    ):
        buffer = BytesIO()
        dataset.to_parquet(buffer, index=False)
        buffer.seek(0)
        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/file",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "dataset_name": dataset_name,
                "description": description,
                "overwrite": overwrite,
            },
            files={
                "file": (
                    f"{dataset_name}.parquet",
                    buffer,
                ),
            },
        )
        if response.status_code != 200:
            raise Exception
        # print(response.text)

    def list_datasets(self) -> List[str]:
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={"detailed": "false"},
        )

        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        return response.json()

    def retrieve_dataset(self, dataset_name: str) -> pd.DataFrame:
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/{dataset_name}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "file_format": "json",
            },
        )
        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        response_json = response.json()
        response_json_keys = response_json.keys()
        if "metadata" not in response_json_keys:
            raise Exception
        if "data" not in response_json_keys:
            raise Exception

        data = pd.DataFrame(eval(response_json["data"]))

        return data, response_json["metadata"]

    def delete_datasets(self, dataset_names: List[str]) -> None:
        response = requests.delete(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/delete",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "dataset_names": dataset_names,
            },
        )
        assert response.status_code == 200, f"Status code mismatch: {response.text}"

    def list_example_datasets(self) -> List[str]:
        return self.example_dataset_names

    def retrieve_example_dataset(self, dataset_name: str) -> Tuple[pd.DataFrame, Dict]:
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/datasets/example/{dataset_name}",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "file_format": "json",
            },
        )
        assert response.status_code == 200, f"Status code mismatch: {response.text}"
        response_json = response.json()
        response_json_keys = response_json.keys()
        if "metadata" not in response_json_keys:
            raise Exception
        if "data" not in response_json_keys:
            raise Exception

        data = pd.DataFrame(eval(response_json["data"]))

        return data, response_json["metadata"]

    def apply_feature_function_to_dataset(
        self,
        feature_function_name: str,
        original_datasets: List[str],
        generated_dataset_name: Optional[str] = None,
        generated_dataset_description: Optional[str] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        process_synchronously: bool = True,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Applies a feature function to existing data.

        Args:
            feature_function_name (str): The name of the feature function to apply.
            original_datasets (List[str]): A list of dataset names to apply the function to
            generated_dataset_name (Optional[str], optional): A name for the generated dataset. Defaults to None.
            generated_dataset_description (Optional[str], optional): A description for the generated dataset. Defaults to None.
            kwargs (Optional[Dict[str, Any]], optional): Keyword arguments for the feature function. Defaults to None.
            overwrite (bool, optional): Whether to overwrite an existing dataset. Defaults to True.

        Returns:
            Dict[str, Any]: A dict with the response message and, if any, task_ids.
        """
        instruction = {
            "feature_function_name": feature_function_name,
            "original_datasets": original_datasets,
            "generated_dataset_name": generated_dataset_name,
            "generated_dataset_description": generated_dataset_description,
            "feature_function_kwargs": kwargs or {},
        }
        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/apply_to_dataset",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "process_synchronously": process_synchronously,
                "overwrite": overwrite,
            },
            json=[instruction],
        )
        return response.json()

    def apply_feature_function_to_data(
        self,
        data: pd.DataFrame,
        feature_function_name: str,
        generated_dataset_name: Optional[str] = None,
        generated_dataset_description: Optional[str] = None,
        kwargs: Optional[Dict[str, Any]] = None,
        process_synchronously: bool = True,
        overwrite: bool = True,
    ) -> pd.DataFrame:
        buffer = BytesIO()
        data.to_parquet(buffer, index=False)
        buffer.seek(0)
        fake_path = f"{generated_dataset_name}_origin.parquet"
        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/apply_to_file",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
                # "Content-Type": "application/json",
            },
            params={
                "feature_function_name": feature_function_name,
                "generated_dataset_name": generated_dataset_name,
                "generated_dataset_description": generated_dataset_description,
                "feature_function_kwargs_str": json.dumps(kwargs),
                "process_synchronously": process_synchronously,
                "overwrite": overwrite,
            },
            files={
                "file": (
                    fake_path,
                    buffer,
                ),
            },
        )

        if response.status_code != 200:
            print(response.status_code, response.text)
            raise Exception

        return response.json()

    def list_feature_functions(
        self,
        detailed: bool = False,
        must_contain_all_tags: bool = False,
        tags: List[str] = [],
    ) -> List[Dict[str, Any]]:
        """
        Lists available feature functions on the server.

        Args:
            detailed (bool, optional): Whether to include detailed information about each feature function. Defaults to False.

        Returns:
            List[Dict[str, Any]]: List of feature functions.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "detailed": detailed,
                "must_contain_all_tags": must_contain_all_tags,
                "tags": tags,
            },
        )
        return response.json()

    def list_available_feature_functions_tags(self) -> List[str]:
        """
        Lists all available tags for feature functions.

        Returns:
            List[str]: List of tags.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/functions/tags",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )

        if response.status_code != 200:
            if "tags" not in response.json().keys():
                raise Exception(f"Status code mismatch: {response.text}")
            else:
                print("Warning", response.status_code, response.text)
                return response.json()["tags"]

        tags = response.json()["tags"]
        return tags

    def list_available_recipes_tags(self) -> List[str]:
        """
        Lists all available tags for recipes.

        Returns:
            List[str]:  A list of all available recipe tags.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/recipes/tags",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )

        if response.status_code != 200:
            if "tags" not in response.json().keys():
                raise Exception(f"Status code mismatch: {response.text}")
            else:
                print("Warning", response.status_code, response.text)
                return response.json()["tags"]

        return response.json()["tags"]

    def list_recipes(self, df: pd.DataFrame | None = None) -> List[str]:  # FIXME
        """
        Lists available recipes on the server.

        Returns:
            List[str]:  A list of recipe names.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/recipes/list",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )
        return response.json()

    def apply_recipe_to_dataset(
        self,
        recipe_name: str,
        original_dataset: str,
        generated_dataset_name: Optional[str] = None,
        generated_dataset_description: Optional[str] = None,
        process_synchronously: bool = True,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Applies a recipe to existing datasets.

        Args:
            recipe_name (str): The name of the recipe to apply.
            original_datasets (List[str]): A list of dataset names to apply the recipe to.
            generated_dataset_name (Optional[str], optional): A name for the generated dataset. Defaults to None.
            generated_dataset_description (Optional[str], optional): A description for the generated dataset. Defaults to None.
            process_synchronously (bool, optional): Whether to process synchronously or asynchronously. Defaults to True.
            overwrite (bool, optional): Whether to overwrite an existing dataset. Defaults to True.

        Returns:
            Dict[str, Any]: A dictionary indicating the status of the operation, including task IDs if processed asynchronously.
        """

        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/recipes/apply_to_dataset",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "recipe_name": recipe_name,
                "original_dataset": original_dataset,
                "generated_dataset_name": generated_dataset_name,
                "generated_dataset_description": generated_dataset_description,
                "process_synchronously": process_synchronously,
                "overwrite": overwrite,
            },
        )
        return response

    def apply_recipe_to_data(
        self,
        recipe_name: str,
        data: pd.DataFrame,
        generated_dataset_name: Optional[str] = None,
        generated_dataset_description: Optional[str] = None,
        process_synchronously: bool = True,
        overwrite: bool = True,
    ) -> Dict[str, Any]:
        """
        Applies a recipe to a dataframe, creating a new dataset.

        Args:
            recipe_name (str): The name of the recipe to apply.
            data: The input data as a Pandas DataFrame.
            generated_dataset_name (Optional[str], optional): The name for the new dataset generated.
                If not provided, defaults to the recipe_name. Defaults to None.
            generated_dataset_description (Optional[str], optional): An optional description for the new dataset.
                Defaults to None.
            process_synchronously (bool, optional): If True, the function is applied immediately, and the
                response includes the result of the application. If False, a background task is created, and
                the response includes a task ID. Defaults to True.
            overwrite (bool, optional): If True, overwrites an existing dataset with the same name. Defaults to True.

        Returns:
            Dict[str, Any]: A dictionary containing the message about the operation's success. If processed
            asynchronously, it will also include the `task_id` (list of strings) of the background task(s).

        Raises:
            Exception: If recipe not found or the server request did not succeed.
        """

        available_recipes = self.list_recipes()
        if recipe_name not in available_recipes:
            raise Exception(f"Recipe '{recipe_name}' not found.")

        response = requests.post(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/recipes/apply_recipe_to_file",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            data={
                "recipe_name": recipe_name,
                "data": data.to_json(orient="records"),
                "generated_dataset_name": generated_dataset_name or recipe_name,
                "generated_dataset_description": generated_dataset_description,
            },
            params={
                "process_synchronously": process_synchronously,
                "overwrite": overwrite,
            },
        )

        if response.status_code != 200:
            raise Exception(
                f"Failed to apply recipe. Status Code: {response.status_code}, Message: {response.text}"
            )

        return response#.json()

    def list_trained_models(self) -> List[str]:
        """Lists the available trained ML models.

        Returns:
            List[str]: A list of model names.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/machinelearning/models",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
        )
        return response.json()

    def get_training_info(self, model_name: str) -> Dict[str, Any]:
        """Retrieves training information for a specific model.

        Args:
            model_name (str): The name of the model.

        Returns:
            Dict: Training information as a JSON response.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/machinelearning/training_info",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "model_name": model_name,
            },
        )
        return response.json()

    def generate_synthetic_data(
        self,
        model_name: str,
        number_of_examples: int,
        file_format: str = "json",
        single_file: bool = False,
    ) -> Union[List[Dict[str, Any]], requests.Response]:
        """Generates synthetic data using a specified model.

        Args:
            model_name (str): The name of the trained model.
            number_of_examples (int): The number of examples to generate.
            file_format (str, optional): The desired file format ('json', 'csv', 'parquet'). Defaults to 'json'.
            single_file (bool, optional): Whether to return a single file or multiple files. Defaults to False.

        Returns:
            Union[List[Dict[str, Any]], Response]: If file_format is 'json', returns a list of dictionaries.
            Otherwise, returns a Response object.
        """
        response = requests.get(
            verify=self.verify_requests,
            url=f"https://{self.url}/v1/machinelearning/generate",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "model_name": model_name,
                "number_of_examples": number_of_examples,
                "file_format": file_format,
                "single_file": single_file,
            },
        )
        if file_format == "json":
            return response.json()
        else:
            return response

    def train_model(
        self,
        dataset_name: str,
        model_name: str = "test_model",
        index_col: str = "timestamp",
        epochs: int = 10,
        batch_size: int = 1000,
        sequence_len: int = 2,
        add_sin_cos: bool = True,
        overwrite: bool = False,
        synchronously: bool = True,
    ) -> Dict[str, Any]:
        """
        Trains a Gretel DoppelGANger model on the specified dataset.

        Args:
            dataset_name (str): The name of the dataset to use for training.
            model_name (str, optional): The name to assign to the trained model. Defaults to "test_model".
            index_col (str, optional): Name of the column to use as index.  Defaults to "timestamp".
            epochs (int, optional): The number of training epochs. Defaults to 10.
            batch_size (int, optional): The batch size for training. Defaults to 1000.
            sequence_len (int, optional): The length of sequences to divide the dataset
                into for training.  Defaults to 2.
            add_sin_cos (bool, optional): Whether to add sin/cos features for hour and month.
                Defaults to True.
            overwrite (bool, optional): Whether to overwrite an existing model with the same name.
                Defaults to False.
            synchronously (bool, optional): Whether to wait for the training to complete before returning,
                or to run training in the background. Defaults to True.

        Returns:
            Dict[str, Any]: A dictionary containing the status of the training operation. If training
            is synchronous, this will include a success/failure message.  If asynchronous,
            it will include a task ID for monitoring the background task.

        Raises:
            HTTPException: If there is an error during training, such as a problem with the input data
                or if a model with the given name already exists and `overwrite` is False.
        """
        response = requests.post(
            f"http://{self.url}/v1/machinelearning/train",
            headers={
                "Authorization": f"Bearer {self.token}",
                "accept": "application/json",
            },
            params={
                "model_name": model_name,
                "dataset_name": dataset_name,
                "synchronously": synchronously,
                "batch_size": batch_size,
                "epochs": epochs,
                "index_col": index_col,
                "overwrite": overwrite,
                "sequence_len": sequence_len,
                "add_sin_cos": add_sin_cos,
            },
            verify=self.verify_requests,
        )

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(
                f"Error training model: {response.status_code} {response.text}",
            )

        return response.json()


if __name__ == "__main__":
    from dotenv import load_dotenv
    import os

    load_dotenv(verbose=True)

    BASE_URL = os.getenv("BASE_URL", None)
    USER_TOKEN = os.getenv("USER_TOKEN", None)

    client = VoltusClient(BASE_URL, USER_TOKEN, verify_requests=True)

    # user_json = client.get_current_authenticated_user()
    # print(user_json)

    # df = pd.read_csv(
    #     "C:/Users/carlos.t.santos/Desktop/Files/Reps/feature-store/clients/python-client/python_client/energy_data.csv"
    # )
    # client.add_dataset(df)

    dataset_names = client.list_datasets()
    for dataset_name in dataset_names:
        print(dataset_name)

    # client.retrieve_dataset(dataset_names[0])
