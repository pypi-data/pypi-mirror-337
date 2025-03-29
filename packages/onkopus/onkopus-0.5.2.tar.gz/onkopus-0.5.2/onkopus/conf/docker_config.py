
tag = "main"

available_modules = ["dbsnp","clinvar","seqcat","dbnsfp","gencode","civic","oncokb",
                     "metakb","protein_analysis","molecular_features","drug_classification",
                     "aggregator","interpreter","drug_gene_interactions", "cache",
                     "server", "web", "database"]

module_ids = {
    "dbsnp": ["dbsnp.yml"],
    "clinvar": ["clinvar.yml"],
    "uta": ["uta-adapter.yml", "uta-database.yml"],
    "fathmm": ["fathmm-adapter.yml"],
    "m3d": ["m3dapp.yml"],
    "uniprot": ["uniprot-adapter.yml"],
    "vep": ["vep-adapter.yml"],
    "vus-predict": ["vus-predict.py"],
    "revel": ["revel.yml"],
    "loftool": ["loftool.yml"],
    "onkopus-server": ["onkopus-server.yml"],
    "onkopus-web": ["onkopus-web.yml"],
    "metakb": ["metakb-adapter.yml"],
    "oncokb": ["oncokb-adapter.yml"],
    "civic": ["civic-db.yml", "civic-adapter.yml"],
    "dbnsfp": ["dbnsfp-adapter.yml"],
    "primateai": ["primateai-adapter.yml"],
    "onkopus-database": ["onkopus-database.yml"],
    "onkopus-websocket-server": ["onkopus-server.yml"],
    "onkopus-cache":["onkopus-cache.yml"],
    "protein-analysis":["protein-analysis.yml"],
    "molecular-features":["molecular-features.yml"],
    "onkopus-aggregator":["onkopus-aggregator.yml"],
    "onkopus-interpreter":["onkopus-interpreter.yml"],
    "gencode":["gencode-adapter.yml", "gencode-db.yml"]
}
