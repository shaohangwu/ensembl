from functools import singledispatchmethod
from urllib.parse import urljoin

import requests


class Ensembl:
    headers = {"content-type": "application/json"}

    def __init__(self, assembly="GRCh38"):
        self.session = requests.Session()
        if assembly == "GRCh38":
            self.server = "https://rest.ensembl.org"
        elif assembly == "GRCh37":
            self.server = "https://grch37.rest.ensembl.org"

    def get(self, endpoint, params):
        response = self.session.get(urljoin(self.server, endpoint), headers=self.headers, params=params)
        return response.json()

    def post(self, endpoint, params, json):
        response = self.session.post(urljoin(self.server, endpoint), headers=self.headers, params=params, json=json)
        return response.json()

    @singledispatchmethod
    def variant_recoder(self, id: str, **kwargs):
        return self.get(endpoint=f"variant_recoder/human/{id}", params=kwargs)

    @variant_recoder.register
    def _(self, id: list, **kwargs):
        return self.post(endpoint=f"variant_recoder/human", params=kwargs, json={"ids": id})

    @singledispatchmethod
    def variation(self, id: str, **kwargs):
        return self.get(endpoint=f"variation/human/{id}", params=kwargs)

    @variation.register
    def _(self, id: list, **kwargs):
        return self.post(endpoint="variation/human", params=kwargs, json={"ids": id})

    def variation_pmcid(self, pmcid):
        return self.get(endpoint=f"variation/human/pmcid/{pmcid}")

    def variation_pmid(self, pmid):
        return self.get(endpoint=f"variation/human/pmid/{pmid}")

    @singledispatchmethod
    def vep_hgvs(self, hgvs: str, **kwargs):
        return self.get(endpoint=f"vep/human/hgvs/{hgvs}", params=kwargs)

    @vep_hgvs.register
    def _(self, hgvs: list, **kwargs):
        return self.post(endpoint="vep/human/hgvs", params=kwargs, json={"hgvs_notations": hgvs})

    @singledispatchmethod
    def vep_id(self, id: str, **kwargs):
        return self.get(endpoint=f"vep/human/id/{id}", params=kwargs)

    @vep_id.register
    def _(self, id: list, **kwargs):
        return self.post(endpoint="vep/human/id", params=kwargs, json={"ids": id})


if __name__ == "__main__":
    import pprint

    ensembl = Ensembl()
    pprint.pprint(ensembl.variation_pmid(11586351))
