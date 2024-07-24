import polars as pl
from Bio import Entrez
from broad_babel.query import get_mapper

Entrez.email = "amunozgo@broadinstitute.org"


def genes_to_summaries(genes: tuple[str]) -> pl.DataFrame:
    # %% Convert to entrez ids using broad_babel
    ids = get_mapper(
        query=genes,
        input_column="standard_key",
        output_columns="standard_key,NCBI_Gene_ID",
    )

    # %% Fetch summaries
    entries = []
    fields = (
        "Name",
        "Description",
        "Summary",
        "OtherDesignations",
    )
    for id_ in ids.values():
        print(id_)
        stream = Entrez.esummary(db="gene", id=id_)
        record = Entrez.read(stream)

        entries.append(
            {k: record["DocumentSummarySet"]["DocumentSummary"][0][k] for k in fields}
        )

    # %% Show the columns in a nice way
    df = pl.DataFrame(entries)
    return df
