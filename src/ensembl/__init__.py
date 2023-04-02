from functools import singledispatchmethod
from urllib.parse import urljoin

import requests


class Ensembl:
    headers = {"content-type": "application/json"}

    def __init__(self, assembly="GRCh38"):
        self.session = requests.Session()
        if assembly == "GRCh38":
            self.server = "http://rest.ensembl.org"
        elif assembly == "GRCh37":
            self.server = "http://grch37.rest.ensembl.org"

    def get(self, endpoint, params):
        response = self.session.get(urljoin(self.server, endpoint), headers=self.headers, params=params)
        return response.json()

    def post(self, endpoint, params, json):
        response = self.session.post(urljoin(self.server, endpoint), headers=self.headers, params=params, json=json)
        return response.json()

    @singledispatchmethod
    def archive(self, id: str, **kwargs):
        """Uses the given identifier to return its latest version"""
        return self.get(endpoint=f"archive/id/{id}", params=kwargs)

    @archive.register
    def _(self, id: list, **kwargs):
        """Retrieve the latest version for a set of identifiers"""
        return self.post(endpoint=f"archive/id", json={"id": id}, params=kwargs)

    def cafe_genetree_id(self, id, **kwargs):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        return self.get(endpoint=f"cafe/genetree/id/{id}", params=kwargs)

    def cafe_genetree_member_id(self, id, **kwargs):
        """Retrieves the cafe tree of the gene tree that contains the gene / transcript / translation stable identifier"""
        return self.get(endpoint=f"cafe/genetree/member/id/{id}", params=kwargs)

    def cafe_genetree_member_symbol(self, symbol, species="human", **kwargs):
        """Retrieves the cafe tree of the gene tree that contains the gene identified by a symbol"""
        return self.get(endpoint=f"cafe/genetree/member/symbol/{species}/{symbol}", params=kwargs)

    def genetree_id(self, id, **kwargs):
        """Retrieves a gene tree for a gene tree stable identifier"""
        return self.get(endpoint=f"genetree/id/{id}", params=kwargs)

    def genetree_member_id(self, id, **kwargs):
        """Retrieves the gene tree that contains the gene / transcript / translation stable identifier"""
        return self.get(endpoint=f"genetree/member/id/{id}", params=kwargs)

    def genetree_member_symbol(self, species, symbol, **kwargs):
        """Retrieves the gene tree that contains the gene identified by a symbol"""
        return self.get(endpoint=f"genetree/member/symbol/{species}/{symbol}", params=kwargs)

    def alignment_region(self, species, region, **kwargs):
        """Retrieves genomic alignments as separate blocks based on a region and species"""
        return self.get(endpoint=f"alignment/region/{species}/{region}", params=kwargs)

    def homology_id(self, id, **kwargs):
        """Retrieves homology information (orthologs) by Ensembl gene id"""
        return self.get(endpoint=f"homology/id/{id}", params=kwargs)

    def homology_symbol(self, species, symbol, **kwargs):
        """Retrieves homology information (orthologs) by symbol"""
        return self.get(f"homology/symbol/{species}/{symbol}", params=kwargs)

    def xrefs_symbol(self, species, symbol, **kwargs):
        """Looks up an external symbol and returns all Ensembl objects linked to it.
        This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference.
        If a gene's transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links)."""
        return self.get(f"xrefs/symbol/{species}/{symbol}", params=kwargs)

    def xrefs_id(self, id, **kwargs):
        """Perform lookups of Ensembl Identifiers and retrieve their external references in other databases"""
        return self.get(f"xrefs/id/{id}", params=kwargs)

    def xrefs_name(self, species, name, **kwargs):
        """Performs a lookup based upon the primary accession or display label of an external reference and returning the information we hold about the entry"""
        return self.get(f"xrefs/name/{species}/{name}", params=kwargs)

    def info_analysis(self, species, **kwargs):
        """List the names of analyses involved in generating Ensembl data."""
        return self.get(f"info/analysis/{species}", params=kwargs)

    def info_assembly(self, species, **kwargs):
        """List the currently available assemblies for a species, along with toplevel sequences, chromosomes and cytogenetic bands."""
        return self.get(f"info/assembly/{species}", params=kwargs)

    def info_assembly_region_name(self, species, region_name, **kwargs):
        """Returns information about the specified toplevel sequence region for the given species."""
        return self.get(f"info/assembly/{species}/{region_name}", params=kwargs)

    def info_biotypes(self, species, **kwargs):
        """List the functional classifications of gene models that Ensembl associates with a particular species.
        Useful for restricting the type of genes/transcripts retrieved by other endpoints."""
        return self.get(f"info/biotypes/{species}", params=kwargs)

    def info_biotypes_groups(self, **kwargs):
        """Without argument the list of available biotype groups is returned.
        With :group argument provided, list the properties of biotypes within that group.
        Object type (gene or transcript) can be provided for filtering."""
        return self.get(f"info/biotypes/groups", params=kwargs)

    def info_biotypes_name(self, name, **kwargs):
        """List the properties of biotypes with a given name. Object type (gene or transcript) can be provided for filtering."""
        return self.get(f"info/biotypes/name/{name}", params=kwargs)

    def info_compara_methods(self, **kwargs):
        """List all compara analyses available (an analysis defines the type of comparative data)."""
        return self.get(f"info/compara/methods", params=kwargs)

    def info_compara_species_sets(self, method, **kwargs):
        """List all collections of species analysed with the specified compara method."""
        return self.get(f"info/compara/species_sets/{method}", params=kwargs)

    def info_comparas(self, **kwargs):
        """Lists all available comparative genomics databases and their data release."""
        return self.get(f"info/comparas", params=kwargs)

    def info_data(self, **kwargs):
        """Shows the data releases available on this REST server."""
        return self.get(f"info/data", params=kwargs)

    def info_eg_version(self, **kwargs):
        """Returns the Ensembl Genomes version of the databases backing this service"""
        return self.get("info/eg_version", params=kwargs)

    def info_external_dbs(self, species, **kwargs):
        """Lists all available external sources for a species."""
        return self.get(f"info/external_dbs/{species}", params=kwargs)

    def info_divisions(self, **kwargs):
        """Get list of all Ensembl divisions for which information is available"""
        return self.get("info/divisions", params=kwargs)

    def info_genomes(self, name, **kwargs):
        """Find information about a given genome"""
        return self.get(f"info/genomes/{name}", params=kwargs)

    def info_genomes_accession(self, accession, **kwargs):
        """Find information about genomes containing a specified INSDC accession"""
        return self.get(f"info/genomes/accession/{accession}", params=kwargs)

    def info_genomes_assembly(self, assembly_id, **kwargs):
        """Find information about a genome with a specified assembly"""
        return self.get(f"info/genomes/assembly/{assembly_id}", params=kwargs)

    def info_genomes_division(self, division, **kwargs):
        """Find information about all genomes in a given division. May be large for Ensembl Bacteria."""
        return self.get(f"info/genomes/division/{division}", params=kwargs)

    def info_genomes_taxonomy(self, taxon_name, **kwargs):
        """Find information about all genomes beneath a given node of the taxonomy"""
        return self.get(f"info/genomes/taxonomy/{taxon_name}", params=kwargs)

    def info_ping(self, **kwargs):
        """Checks if the service is alive."""
        return self.get("info/ping", params=kwargs)

    def info_rest(self, **kwargs):
        """Shows the current version of the Ensembl REST API."""
        return self.get("info/rest", params=kwargs)

    def info_software(self, **kwargs):
        """Shows the current version of the Ensembl API used by the REST server."""
        return self.get("info/software", params=kwargs)

    def info_species(self, **kwargs):
        """Lists all available species, their aliases, available adaptor groups and data release."""
        return self.get("info/species", params=kwargs)

    def info_variation(self, species, **kwargs):
        """List the variation sources used in Ensembl for a species."""
        return self.get(f"info/variation/{species}", params=kwargs)

    def info_variation_consequence_types(self, **kwargs):
        """Lists all variant consequence types."""
        return self.get(f"info/variation/consequence_types", params=kwargs)

    def info_variation_populations(self, species, population_name, **kwargs):
        """List all individuals for a population from a species"""
        return self.get(f"info/variation/populations/{species}/{population_name}", params=kwargs)

    def info_variation_species(self, species, **kwargs):
        """List all populations for a species"""
        return self.get(f"info/variation/populations/{species}", params=kwargs)

    def ld(self, species, id, population_name, **kwargs):
        """Computes and returns LD values between the given variant and all other variants in a window centered around the given variant.
        The window size is set to 500 kb."""
        return self.get(f"ld/{species}/{id}/{population_name}", params=kwargs)

    def ld_pairwise(self, species, id1, id2, **kwargs):
        """Computes and returns LD values between the given variants."""
        return self.get(f"ld/{species}/pairwise/{id1}/{id2}", params=kwargs)

    def ld_region(self, species, region, population_name, **kwargs):
        """Computes and returns LD values between all pairs of variants in the defined region."""
        return self.get(f"ld/{species}/region/{region}/{population_name}", params=kwargs)

    @singledispatchmethod
    def lookup_id(self, id: str, **kwargs):
        """Find the species and database for a single identifier e.g. gene, transcript, protein"""
        return self.get(endpoint=f"lookup/id/{id}", params=kwargs)

    @lookup_id.register
    def _(self, id: list, **kwargs):
        """Find the species and database for several identifiers. IDs that are not found are returned with no data."""
        return self.post(endpoint=f"lookup/id", params=kwargs, json={"ids": id})

    @singledispatchmethod
    def lookup_symbol(self, symbol: str, species="human", **kwargs):
        """Find the species and database for a symbol in a linked external database"""
        return self.get(f"lookup/symbol/{species}/{symbol}", params=kwargs)

    @lookup_symbol.register
    def _(self, symbol: list, species="human", **kwargs):
        """Find the species and database for a set of symbols in a linked external database. Unknown symbols are omitted from the response."""
        return self.post(f"lookup/symbol/{species}", params=kwargs, json={"symbols": symbol})

    def map_cdna(self, id, region, **kwargs):
        """Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        return self.get(f"map/cdna/{id}/{region}", params=kwargs)

    def map_cds(self, id, region, **kwargs):
        """Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        return self.get(f"map/cds/{id}/{region}", params=kwargs)

    def map_assembly(self, species, asm_one, region, asm_two, **kwargs):
        """Convert the co-ordinates of one assembly to another"""
        return self.get(f"map/{species}/{asm_one}/{region}/{asm_two}", params=kwargs)

    def map_translation(self, id, region, **kwargs):
        """Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
        return self.get(f"map/translation/{id}/{region}", params=kwargs)

    def ontology_ancestors(self, id, **kwargs):
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships"""
        return self.get(f"ontology/ancestors/{id}", params=kwargs)

    def ontology_ancestors_chart(self, id, **kwargs):
        """Reconstruct the entire ancestry of a term from is_a and part_of relationships"""
        return self.get(f"ontology/ancestors/chart/{id}", params=kwargs)

    def ontology_descendants(self, id, **kwargs):
        """Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier"""
        return self.get(f"ontology/descendants/{id}", params=kwargs)

    def ontology_id(self, id, **kwargs):
        """Search for an ontological term by its namespaced identifier"""
        return self.get(f"ontology/id/{id}", params=kwargs)

    def ontology_name(self, name, **kwargs):
        """Search for a list of ontological terms by their name"""
        return self.get(f"ontology/name/{name}", params=kwargs)

    def taxonomy_classification(self, id, **kwargs):
        """Return the taxonomic classification of a taxon node"""
        return self.get(f"taxonomy/classification/{id}", params=kwargs)

    def taxonomy_id(self, id, **kwargs):
        """Search for a taxonomic term by its identifier or name"""
        return self.get(f"taxonomy/id/{id}", params=kwargs)

    def taxonomy_name(self, name, **kwargs):
        """Search for a taxonomic id by a non-scientific name"""
        return self.get(f"taxonomy/name/{name}", params=kwargs)

    def overlap_id(self, id, **kwargs):
        """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a region defined by the given identifier."""
        return self.get(f"overlap/id/{id}", params=kwargs)

    def overlap_region(self, species, region, **kwargs):
        """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a given region."""
        return self.get(f"overlap/region/{species}/{region}", params=kwargs)

    def overlap_translation(self, id, **kwargs):
        """Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variants)."""
        return self.get(f"overlap/translation/{id}", params=kwargs)

    def phenotype_accession(self, species, accession, **kwargs):
        """Return phenotype annotations for genomic features given a phenotype ontology accession"""
        return self.get(f"phenotype/accession/{species}/{accession}", params=kwargs)

    def phenotype_gene(self, species, gene, **kwargs):
        """Return phenotype annotations for a given gene."""
        return self.get(f"phenotype/gene/{species}/{gene}", params=kwargs)

    def phenotype_region(self, species, region, **kwargs):
        """Return phenotype annotations that overlap a given genomic region."""
        return self.get(f"phenotype/region/{species}/{region}", params=kwargs)

    def phenotype_term(self, species, term, **kwargs):
        """Return phenotype annotations for genomic features given a phenotype ontology term"""
        return self.get(f"phenotype/term/{species}/{term}", params=kwargs)

    def regulatory_microarray_vendor(self, species, microarray, vendor, **kwargs):
        """Returns information about a specific microarray"""
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/vendor/{vendor}", params=kwargs)

    def regulatory_species(self, species, **kwargs):
        """Returns information about all epigenomes available for the given species"""
        return self.get(f"regulatory/species/{species}/epigenome", params=kwargs)

    def species_binding_matrix(self, species, binding_matrix_stable_id, **kwargs):
        """Return the specified binding matrix"""
        return self.get(f"species/{species}/binding_matrix/{binding_matrix_stable_id}", params=kwargs)

    def regulatory_microarray(self, species, **kwargs):
        """Returns information about all microarrays available for the given species"""
        return self.get(f"regulatory/species/{species}/microarray", params=kwargs)

    def regulatory_probe(self, species, microarray, probe, **kwargs):
        """Returns information about a specific probe from a microarray"""
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe}", params=kwargs)

    def regulatory_probe_set(self, species, microarray, probe_set, **kwargs):
        """Returns information about a specific probe_set from a microarray"""
        return self.get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe_set}", params=kwargs)

    def regulatory_id(self, species, id, **kwargs):
        """Returns a RegulatoryFeature given its stable ID (e.g. ENSR00000082023)"""
        return self.get(f"regulatory/species/{species}/id/{id}", params=kwargs)

    @singledispatchmethod
    def sequence_id(self, id: str, **kwargs):
        """Request multiple types of sequence by stable identifier. Supports feature masking and expand options."""
        return self.get(f"sequence/id/{id}", params=kwargs)

    @sequence_id.register
    def _(self, id: list, **kwargs):
        """Request multiple types of sequence by a stable identifier list."""
        return self.post(f"sequence/id", json={'ids': id}, params=kwargs)

    @singledispatchmethod
    def sequence_region(self, region: str, species, **kwargs):
        """Returns the genomic sequence of the specified region of the given species. Supports feature masking and expand options."""
        return self.get(f"sequence/region/{species}/{region}", params=kwargs)

    @sequence_region.register
    def _(self, region: list, species, **kwargs):
        """Request multiple types of sequence by a list of regions."""
        return self.post(f"sequence/region/{species}", json={'region': region}, params=kwargs)

    def transcript_haplotypes(self, species, id, **kwargs):
        """Computes observed transcript haplotype sequences based on phased genotype data"""
        return self.get(f"transcript_haplotypes/{species}/{id}", params=kwargs)

    def ga4gh_beacon(self, **kwargs):
        """Return Beacon information"""
        return self.get("ga4gh/beacon", params=kwargs)

    @singledispatchmethod
    def ga4gh_beacon_query(self, query: str, **kwargs):
        """Return the Beacon response for allele information"""
        return self.get(f"ga4gh/beacon/{query}", params=kwargs)

    @ga4gh_beacon_query.register
    def _(self, query: list, **kwargs):
        """Return the Beacon response for allele information"""
        return self.post(f"ga4gh/beacon", json={"query": query}, params=kwargs)

    def ga4gh_features(self, id, **kwargs):
        """Return the GA4GH record for a specific sequence feature given its identifier"""
        return self.get(f"ga4gh/features/{id}", params=kwargs)

    def ga4gh_features_search(self, end, referenceName, start, **kwargs):
        """Return a list of sequence annotation features in GA4GH format"""
        return self.post(f"ga4gh/features/search",
                         json=dict(end=end, referenceName=referenceName, start=start, **kwargs), params={})

    def ga4gh_callsets_search(self, variantSetId, **kwargs):
        """Return a list of sets of genotype calls for specific samples in GA4GH format"""
        return self.post(f"ga4gh/callsets/search", json=dict(variantSetId=variantSetId, **kwargs), params={})

    def ga4gh_callsets(self, id, **kwargs):
        """Return the GA4GH record for a specific CallSet given its identifier"""
        return self.get(f"ga4gh/callsets/{id}", params=kwargs)

    def ga4gh_datasets_search(self, **kwargs):
        """Return a list of datasets in GA4GH format"""
        return self.post(f"ga4gh/datasets/search", json=kwargs, params={})

    def ga4gh_datasets(self, id, **kwargs):
        """Return the GA4GH record for a specific dataset given its identifier"""
        return self.get(f"ga4gh/datasets/{id}", params=kwargs)

    def ga4gh_featuresets_search(self, datasetId, **kwargs):
        """Return a list of feature sets in GA4GH format"""
        return self.post(f"ga4gh/featuresets/search", json=dict(datasetId=datasetId, **kwargs), params={})

    def ga4gh_featuresets(self, id, **kwargs):
        """Return the GA4GH record for a specific featureSet given its identifier"""
        return self.get(f"ga4gh_featuresets/{id}", params=kwargs)

    def ga4gh_variants(self, id, **kwargs):
        """Return the GA4GH record for a specific variant given its identifier."""
        return self.get(f"ga4gh/variants/{id}", params=kwargs)

    def ga4gh_variants_search(self, end, referenceName, start, variantSetId, **kwargs):
        """Return variant call information in GA4GH format for a region on a reference sequence"""
        return self.post(f"ga4gh/variants/search",
                         json=dict(end=end, referenceName=referenceName, start=start, variantSetId=variantSetId,
                                   **kwargs), params={})

    def ga4gh_variantannotations_search(self, variantAnnotationSetId, **kwargs):
        """Return variant annotation information in GA4GH format for a region on a reference sequence"""
        return self.post(f"ga4gh/variantannotations/search",
                         json=dict(variantAnnotationSetId=variantAnnotationSetId, **kwargs), params={})

    def ga4gh_variantsets_search(self, datasetId, **kwargs):
        """Return a list of variant sets in GA4GH format"""
        return self.post(f"ga4gh/variantsets/search", json=dict(datasetId=datasetId, **kwargs), params={})

    def ga4gh_variantsets(self, id, **kwargs):
        """Return the GA4GH record for a specific VariantSet given its identifier"""
        return self.get(f"ga4gh/variantsets/{id}", params=kwargs)

    def ga4gh_references_search(self, referenceSetId, **kwargs):
        """Return a list of reference sequences in GA4GH format"""
        return self.post(f"ga4gh/references/search", json=dict(referenceSetId=referenceSetId, **kwargs), params={})

    def ga4gh_references(self, id, **kwargs):
        """Return data for a specific reference in GA4GH format by id"""
        return self.get(f"ga4gh/references/{id}", params=kwargs)

    def ga4gh_referencesets_search(self, referenceSetId, **kwargs):
        """Return a list of reference sets in GA4GH format"""
        return self.post(f"ga4gh/referencesets/search", json=dict(referenceSetId=referenceSetId, **kwargs), params={})

    def ga4gh_referencesets(self, id, **kwargs):
        """Return data for a specific reference set in GA4GH format"""
        return self.get(f"ga4gh/referencesets/{id}", params=kwargs)

    def ga4gh_variantannotationsets_search(self, variantSetId, **kwargs):
        """Return a list of annotation sets in GA4GH format"""
        return self.post(f"ga4gh/variantannotationsets/search", json=dict(variantSetId=variantSetId, **kwargs),
                         params={})

    def ga4gh_variantannotationsets(self, id, **kwargs):
        """Return meta data for a specific annotation set in GA4GH format"""
        return self.get(f"ga4gh/variantannotationsets/{id}", params=kwargs)

    @singledispatchmethod
    def variant_recoder(self, id: str, **kwargs):
        """Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI"""
        return self.get(endpoint=f"variant_recoder/human/{id}", params=kwargs)

    @variant_recoder.register
    def _(self, id: list, **kwargs):
        """Translate a list of variant identifiers, HGVS notations or genomic SPDI notations to all possible variant IDs, HGVS and genomic SPDI"""
        return self.post(endpoint=f"variant_recoder/human", params=kwargs, json={"ids": id})

    @singledispatchmethod
    def variation(self, id: str, **kwargs):
        """Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        return self.get(endpoint=f"variation/human/{id}", params=kwargs)

    @variation.register
    def _(self, id: list, **kwargs):
        """Uses a list of variant identifiers (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
        return self.post(endpoint="variation/human", params=kwargs, json={"ids": id})

    def variation_pmcid(self, pmcid, **kwargs):
        """Fetch variants by publication using PubMed Central reference number (PMCID)"""
        return self.get(endpoint=f"variation/human/pmcid/{pmcid}", params=kwargs)

    def variation_pmid(self, pmid, **kwargs):
        """Fetch variants by publication using PubMed reference number (PMID)"""
        return self.get(endpoint=f"variation/human/pmid/{pmid}", params=kwargs)

    @singledispatchmethod
    def vep_hgvs(self, hgvs: str, **kwargs):
        """Fetch variant consequences based on a HGVS notation"""
        return self.get(endpoint=f"vep/human/hgvs/{hgvs}", params=kwargs)

    @vep_hgvs.register
    def _(self, hgvs: list, **kwargs):
        """Fetch variant consequences for multiple HGVS notations"""
        return self.post(endpoint="vep/human/hgvs", params=kwargs, json={"hgvs_notations": hgvs})

    @singledispatchmethod
    def vep_id(self, id: str, **kwargs):
        """Fetch variant consequences based on a variant identifier"""
        return self.get(endpoint=f"vep/human/id/{id}", params=kwargs)

    @vep_id.register
    def _(self, id: list, **kwargs):
        """Fetch variant consequences for multiple ids"""
        return self.post(endpoint="vep/human/id", params=kwargs, json={"ids": id})

    @singledispatchmethod
    def vep_region(self, region: str, allele, **kwargs):
        """Fetch variant consequences based on a region"""
        return self.get(endpoint=f"vep/human/region/{region}/{allele}", params=kwargs)

    @vep_region.register
    def _(self, region: list, **kwargs):
        """Fetch variant consequences for multiple regions"""
        return self.post(endpoint="vep/human/region", params=kwargs, json={"variants": region})
