def get_dtype_mapping(source: str, target: str) -> dict[str, str]:
    source = source.lower()
    target = target.lower()

    mapping = {}

    if source == "sap":
        if target == "snowflake":
            mapping = {
                "ACCP": "NUMBER",
                "CHAR": "VARCHAR",
                "CLNT": "VARCHAR",
                "CUKY": "VARCHAR",
                "CURR": "NUMBER",
                "D16D": "NUMBER",
                "D16N": "NUMBER",
                "D16R": "NUMBER",
                "D16S": "NUMBER",
                "D34D": "NUMBER",
                "D34N": "NUMBER",
                "D34R": "NUMBER",
                "D34S": "NUMBER",
                "DATS": "DATE",
                "DEC": "NUMBER",
                "FLTP": "FLOAT",
                "INT1": "NUMBER",
                "INT2": "NUMBER",
                "INT4": "NUMBER",
                "INT8": "NUMBER",
                "LANG": "VARCHAR",
                "LCHR": "VARCHAR",
                "LRAW": "BINARY",
                "NUMC": "NUMBER",
                "QUAN": "NUMBER",
                "RAW": "BINARY",
                "RSTR": "BINARY",
                "SSTR": "VARCHAR",
                "STRG": "BINARY",
                "TIMN": "TIME",
                "TIMS": "TIME",
                "UNIT": "VARCHAR",
                "UTCL": "TIMESTAMP_NTZ",
            }

    return mapping
