import os
import logging
from collections import defaultdict
from typing import List, Tuple, Set

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.document_loaders import (
    UnstructuredMarkdownLoader, UnstructuredFileLoader, PyPDFLoader
)

from config import Settings
from util.file_util import FileUtil
from util.llm_token import num_tokens_from_string

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_token_usage_of_docs(docs: List[Document]) -> int:
    content = ""
    for i in docs:
        content += i.page_content
    return num_tokens_from_string(content)


def raise_exception_if_have_same_name_files(all_files: List[str]):
    fileName_map_amount = defaultdict(lambda: 0)
    for i in all_files:
        file_name = os.path.basename(i)
        if fileName_map_amount[file_name] > 1:
            raise Exception(f'not allowed same name file: {file_name}')
        fileName_map_amount[file_name] += 1


def get_txt_new_docs(
        dir: str,
        already_handled_files: Set[str],
) -> Tuple[List[Document], int]:
    all_txt_files, _ = FileUtil.list_dir_with_suffix(dir, ".txt")
    if not all_txt_files:
        return [], 0
    raise_exception_if_have_same_name_files(all_txt_files)

    new_docs = []
    new_doc_amount = 0
    for file in all_txt_files:
        file_name = os.path.basename(file)
        if file_name in already_handled_files:
            continue

        new_doc_amount += 1
        already_handled_files.add(file_name)

        loader = UnstructuredFileLoader(file)
        pages = loader.load()
        logger.info(
            f'{file_name} will use token amount: {get_token_usage_of_docs(pages)}')
        new_docs.extend(pages)
    return new_docs, new_doc_amount


def get_csv_new_docs(
        dir: str,
        already_handled_files: Set[str],
) -> Tuple[List[Document], int]:
    all_csv_files, _ = FileUtil.list_dir_with_suffix(dir, ".csv")
    if not all_csv_files:
        return [], 0
    raise_exception_if_have_same_name_files(all_csv_files)

    new_docs = []
    new_doc_amount = 0
    for file in all_csv_files:
        file_name = os.path.basename(file)
        if file_name in already_handled_files:
            continue

        new_doc_amount += 1
        already_handled_files.add(file_name)

        loader = CSVLoader(file_path=file)
        pages = loader.load()
        logger.info(
            f'{file_name} will use token amount: {get_token_usage_of_docs(pages)}')
        new_docs.extend(pages)
    return new_docs, new_doc_amount


def get_markdown_new_docs(
        dir: str,
        already_handled_files: Set[str],
) -> Tuple[List[Document], int]:
    all_md_files, _ = FileUtil.list_dir_with_suffix(dir, ".md")
    if not all_md_files:
        return [], 0
    raise_exception_if_have_same_name_files(all_md_files)

    new_docs = []
    new_doc_amount = 0
    for file in all_md_files:
        file_name = os.path.basename(file)
        if file_name in already_handled_files:
            continue

        new_doc_amount += 1
        already_handled_files.add(file_name)

        loader = UnstructuredMarkdownLoader(file)
        pages = loader.load()
        logger.info(
            f'{file_name} will use token amount: {get_token_usage_of_docs(pages)}')
        new_docs.extend(pages)
    return new_docs, new_doc_amount


def get_pdf_new_docs(
        dir: str,
        already_handled_files: Set[str],
) -> Tuple[List[Document], int]:
    all_pdf_files, _ = FileUtil.list_dir_with_suffix(dir, ".pdf")
    if not all_pdf_files:
        return [], 0
    raise_exception_if_have_same_name_files(all_pdf_files)

    new_docs = []
    new_doc_amount = 0
    for file in all_pdf_files:
        file_name = os.path.basename(file)
        if file_name in already_handled_files:
            continue

        new_doc_amount += 1
        already_handled_files.add(file_name)
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()
        logger.info(
            f'{file_name} will use token amount: {get_token_usage_of_docs(pages)}')
        new_docs.extend(pages)
    return new_docs, new_doc_amount


def prepare_paper_and_get_chromaDBClient(conf: Settings) -> Chroma:
    logger.info("start indexing files")
    # load已经索引过的文档
    already_embedded_file = 'already_embedded.json'
    exist, err = FileUtil.check_exist(already_embedded_file)
    if err:
        raise Exception(err)
    already_embedded_fileNames = set()
    if exist:
        data = FileUtil.json_load_file(already_embedded_file)
        already_embedded_fileNames = set(data)
    logger.info(
        f'already indexed file amount: {len(already_embedded_fileNames)}\n')

    # 创建embedding相关初试资源
    embeddings = OpenAIEmbeddings(
        openai_api_key=conf.openai_api_key, chunk_size=conf.embedding_chunk_size)
    persist_directory = 'db/chroma_paleontology'
    chroma_collection_name = "local_test"
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embeddings,
                collection_name=chroma_collection_name)

    paper_dir = './static'

    # 开始添加文档进入embedding
    total_new_docs = []
    total_new_file_amount = 0

    # pdf
    logger.info(f'start parsing pdf files')
    new_pdf_docs, new_pdf_file_amount = get_pdf_new_docs(
        paper_dir, already_embedded_fileNames)
    total_new_file_amount += new_pdf_file_amount
    total_new_docs.extend(new_pdf_docs)
    logger.info(
        f'finished parsing pdf files. have {new_pdf_file_amount} new file need to index\n')

    # markdown
    logger.info(f'start parsing markdown files')
    new_md_docs, new_md_file_amount = get_markdown_new_docs(
        paper_dir, already_embedded_fileNames)
    total_new_file_amount += new_md_file_amount
    total_new_docs.extend(new_md_docs)
    logger.info(
        f'finished parsing markdown files. have {new_md_file_amount} new file need to index\n')

    # json

    # csv
    logger.info(f'start parsing csv files')
    new_csv_docs, new_csv_file_amount = get_csv_new_docs(
        paper_dir, already_embedded_fileNames)
    total_new_file_amount += new_csv_file_amount
    total_new_docs.extend(new_csv_docs)
    logger.info(
        f'finished parsing csv files. have {new_csv_file_amount} new file need to index\n')

    # txt
    logger.info(f'start parsing txt files')
    new_txt_docs, new_txt_file_amount = get_txt_new_docs(
        paper_dir, already_embedded_fileNames)
    total_new_file_amount += new_txt_file_amount
    total_new_docs.extend(new_txt_docs)
    logger.info(
        f'finished parsing txt files. have {new_txt_file_amount} new file need to index\n')

    # html

    # persist
    logger.info(f'parsing file finished, start persist to disk')
    if total_new_docs:
        db.add_documents(total_new_docs)
        logger.info(
            f'\tnew need to index file amount: {total_new_file_amount}')
        db.persist()
        FileUtil.json_dump_file(already_embedded_file,
                                list(already_embedded_fileNames))
    else:
        logger.info('no new file need to persist')
    logger.info(f'persist data to disk finished\n')

    logger.info("finished indexing files\n")
    return db


def test_query():
    db = prepare_paper_and_get_chromaDBClient()
    # 开始查询 - 返回问题相关获取到的文本段落
    questions = [
        "brctl命令是用来干嘛的?",
        "chrome extension的manifest.json文件是干嘛的?"
        "Core Data是用来做什么的?",
        "Reds队2012年的工资开销是多少?",
        "GPT-3 每次调用允许多少Tokens?",
    ]

    for index, query in enumerate(questions):
        docs = db.similarity_search(query=query, k=1)

        data = []
        for i in docs:
            data.append(i.page_content)

        context = []
        for i, j in enumerate(data):
            tmp_j = j.replace('\n', '.').replace('<', '[').replace('>', ']')
            context.append(f'{[i+1]}: <{tmp_j}>')

        context = '\n'.join(context)

        final_content = f'''
    you task is to perform the follow actions:
    1 - read the following {len(context)} text delimited by <>
    2 - answer my question only based on those text, if you do't know the answer, just say you don't know. my question is: {query}

    text:
    {context}
        '''
        print(final_content, "\n\n")


if __name__ == "__main__":
    test_query()
