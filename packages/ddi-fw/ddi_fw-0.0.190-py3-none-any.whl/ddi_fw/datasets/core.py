import glob
import logging
from typing import Any, Dict, List, Optional, Type
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, computed_field
from ddi_fw.datasets.dataset_splitter import DatasetSplitter
from ddi_fw.utils.utils import create_folder_if_not_exists


try:
    from ddi_fw.vectorization import SimilarityMatrixGenerator, VectorGenerator
except ImportError:
    raise ImportError(
        "Failed to import vectorization module. Ensure that the module exists and is correctly installed. ")

try:
    from ddi_fw.langchain.embeddings import PoolingStrategy
except ImportError:
    raise ImportError(
        "Failed to import langchain.embeddings module. ")


def stack(df_column):
    return np.stack(df_column.values)


def generate_vectors(df, columns):
    vectorGenerator = VectorGenerator(df)
    generated_vectors = vectorGenerator.generate_feature_vectors(
        columns)
    return generated_vectors


def generate_sim_matrices_new(df, generated_vectors, columns, key_column="id"):
    jaccard_sim_dict = {}
    sim_matrix_gen = SimilarityMatrixGenerator()

    for column in columns:
        # key = '2D_'+column
        key = column
        jaccard_sim_dict[column] = sim_matrix_gen.create_jaccard_similarity_matrices(
            generated_vectors[key])

    similarity_matrices = {}
    keys = df[key_column].to_list()
    new_columns = {}
    for idx in range(len(keys)):
        new_columns[idx] = keys[idx]
    for column in columns:
        new_df = pd.DataFrame.from_dict(jaccard_sim_dict[column])
        new_df = new_df.rename(index=new_columns, columns=new_columns)
        similarity_matrices[column] = new_df
    return similarity_matrices


class BaseDataset(BaseModel):
    dataset_name: str
    index_path: Optional[str] = None
    dataset_splitter_type: Type[DatasetSplitter]
    class_column: str = 'class'
    dataframe: Optional[pd.DataFrame] = None
    X_train: Optional[np.ndarray] = None
    X_test: Optional[np.ndarray] = None
    y_train: Optional[np.ndarray] = None
    y_test: Optional[np.ndarray] = None
    train_indexes: Optional[pd.Index] = None
    test_indexes: Optional[pd.Index] = None
    train_idx_arr: Optional[List[np.ndarray]] = None
    val_idx_arr: Optional[List[np.ndarray]] = None
    columns: List[str] = []

    class Config:
        arbitrary_types_allowed = True

    def produce_inputs(self):
        items = []
        if self.X_train is None or self.X_test is None:
            raise Exception("There is no data to produce inputs")
        y_train_label, y_test_label = np.array(
            self.y_train), np.array(self.y_test)

        if self.columns is None or len(self.columns) == 0:
            items.append([f'default', np.nan_to_num(self.X_train),
                          y_train_label, np.nan_to_num(self.X_test), y_test_label])
        else:
            for index, column in enumerate(self.columns):
                train_data, test_data = self.X_train[:,
                                                     index], self.X_test[:, index]
                items.append([f'{column}', np.nan_to_num(train_data),
                              y_train_label, np.nan_to_num(test_data), y_test_label])

                # items.append([f'{column}_embedding', train_data,
                #             y_train_label, test_data, y_test_label])
        return items

    def produce_inputs_ex(self):
        items = []
        if self.X_train is None or self.X_test is None:
            raise Exception("There is no data to produce inputs")
        y_train_label, y_test_label = stack(self.y_train), stack(self.y_test)

        for column in self.columns:
            train_data, test_data = stack(
                self.X_train[column]), stack(self.X_test[column])
            items.append([f'{column}', np.nan_to_num(train_data),
                          y_train_label, np.nan_to_num(test_data), y_test_label])

            # items.append([f'{column}_embedding', train_data,
            #             y_train_label, test_data, y_test_label])
        return items

    @computed_field
    @property
    def dataset_splitter(self) -> DatasetSplitter:
        return self.dataset_splitter_type()

    def set_dataframe(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    # @abstractmethod
    def prep(self):
        pass

    def load(self):
        """
        Load the dataset. If X_train, y_train, X_test, and y_test are already provided,
        skip deriving them. Otherwise, derive them from the dataframe and indices.
        """
        if self.X_train  and self.y_train and self.X_test and self.y_test :
            # Data is already provided, no need to calculate
            logging.info(
                "X_train, y_train, X_test, and y_test are already provided. Skipping calculation.")
            return
            # return self.X_train, self.X_test, self.y_train, self.y_test, self.train_indexes, self.test_indexes, self.train_idx_arr, self.val_idx_arr

        self.prep()

        if self.index_path is None:
            raise Exception(
                "There is no index path. Please call split_dataset or provide indices.")

        if self.dataframe is None:
            raise Exception("There is no dataframe to derive data from.")

        try:
            train_idx_all, test_idx_all, train_idx_arr, val_idx_arr = self.__get_indexes__(
                self.index_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Index files not found: {e.filename}")

        train = self.dataframe[self.dataframe.index.isin(train_idx_all)]
        test = self.dataframe[self.dataframe.index.isin(test_idx_all)]
        X_train = train.drop(self.class_column, axis=1)
        X_train = train.drop(self.class_column, axis=1)
        y_train = train[self.class_column]
        X_test = test.drop(self.class_column, axis=1)
        y_test = test[self.class_column]
        
        self.X_train = np.array(X_train)
        # self.y_train = np.array(y_train)
        self.y_train = np.array(y_train.tolist())
        self.X_test = np.array(X_test)
        # self.y_test = np.array(y_test)
        self.y_test = np.array(y_test.tolist())

        self.train_indexes = X_train.index
        self.test_indexes = X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr

        # Dataframe to numpy array conversion
       

        # return self.X_train, self.X_test, self.y_train, self.y_test, self.train_indexes, self.test_indexes, self.train_idx_arr, self.val_idx_arr

    def __get_indexes__(self, path):
        train_index_path = path+'/train_indexes.txt'
        test_index_path = path+'/test_indexes.txt'
        train_fold_files = f'{path}/train_fold_*.txt'
        val_fold_files = f'{path}/validation_fold_*.txt'
        train_idx_arr = []
        val_idx_arr = []
        with open(train_index_path, 'r', encoding="utf8") as f:
            train_idx_all = [int(r) for r in f.readlines()]
        with open(test_index_path, 'r', encoding="utf8") as f:
            test_idx_all = [int(r) for r in f.readlines()]

        for filepath in glob.glob(train_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                train_idx = [int(r) for r in f.readlines()]
                train_idx_arr.append(train_idx)
        for filepath in glob.glob(val_fold_files):
            with open(filepath, 'r', encoding="utf8") as f:
                val_idx = [int(r) for r in f.readlines()]
                val_idx_arr.append(val_idx)
        return train_idx_all, test_idx_all, train_idx_arr, val_idx_arr

    def __save_indexes__(self, path, filename, indexes):
        create_folder_if_not_exists(path)
        file_path = path + '/'+filename
        str_indexes = [str(index) for index in indexes]
        with open(file_path, 'w') as f:
            f.write('\n'.join(str_indexes))

    def split_dataset(self, save_indexes: bool = False):
        """
        Split the dataset into training and testing sets. This method is only available
        if a dataframe exists. If X_train, y_train, X_test, and y_test are already present,
        raise an error.
        """
        if self.X_train is not None or self.X_test is not None:
            raise Exception(
                "X_train and X_test are already present. Splitting is not allowed.")

        self.prep()
        if self.dataframe is None:
            raise Exception("There is no dataframe to split.")

        save_path = self.index_path

        X = self.dataframe.drop(self.class_column, axis=1)
        y = self.dataframe[self.class_column]

        X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr = self.dataset_splitter.split(
            X=X, y=y)
        self.X_train = np.array(X_train)
        self.X_test = np.array(X_test)
        self.y_train =  np.array(y_train.tolist())
        self.y_test = np.array(y_test.tolist())
        self.train_indexes = X_train.index
        self.test_indexes = X_test.index
        self.train_idx_arr = train_idx_arr
        self.val_idx_arr = val_idx_arr

       
        if save_indexes:
            # train_pairs = [row['id1'].join(',').row['id2'] for index, row in X_train.iterrows()]
            self.__save_indexes__(
                save_path, 'train_indexes.txt', self.train_indexes.values)
            self.__save_indexes__(
                save_path, 'test_indexes.txt',  self.test_indexes.values)

            for i, (train_idx, val_idx) in enumerate(zip(train_idx_arr, val_idx_arr)):
                self.__save_indexes__(
                    save_path, f'train_fold_{i}.txt', train_idx)
                self.__save_indexes__(
                    save_path, f'validation_fold_{i}.txt', val_idx)

        # return X_train, X_test, y_train, y_test, folds


class TextDatasetMixin(BaseDataset):
    embedding_size: Optional[int] = None
    embedding_dict: Dict[str, Any] = Field(
        default_factory=dict, description="Dictionary for embeddings")
    embeddings_pooling_strategy: PoolingStrategy | None = None

    def process_text(self):
        pass


# class ImageDatasetMixin(BaseModel):
#     image_size: tuple[int, int] = Field(default=(224, 224))
#     augmentations: list[str] = Field(default_factory=list)

#     def process_image_data(self):
#         print(
#             f"Processing image data with size {self.image_size} and augmentations {self.augmentations}...")
