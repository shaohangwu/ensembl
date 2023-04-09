from collections import defaultdict
from functools import singledispatch
from urllib.parse import urljoin

import requests
import pprint

headers = defaultdict(str)
assembly="GRCh38"
scheme="http"
match assembly, scheme:
    case "GRCh38", "http":
        server = "http://rest.ensembl.org"
    case "GRCh37", "http":
        server = "http://grch37.rest.ensembl.org"
    case "GRCh38", "https":
        server = "https://rest.ensembl.org"
    case "GRCh37", "https":
        server = "https://grch37.rest.ensembl.org"

def get(endpoint, params, format):
    session = requests.Session()
    match format:
        case "json":
            headers["Content-Type"] = "application/json"
            response =session.get(urljoin(server, endpoint), headers=headers, params=params)
            return response.json()
        case "xml":
            headers["Content-Type"] = "text/xml"
            response =session.get(urljoin(server, endpoint), headers=headers, params=params)
            return response.text

def post(endpoint, params, json, format):
    session = requests.Session()
    match format:
        case "json":
            headers["Content-Type"] = "application/json"
            response = session.post(urljoin(server, endpoint), headers=headers, params=params, json=json)
            return response.json()
        case "xml":
            headers["Content-Type"] = "text/xml"
            response =session.post(urljoin(server, endpoint), headers=headers, params=params, json=json)
            return response.text
@singledispatch
def archive(id: str, format="json", **kwargs):
    """Uses the given identifier to return its latest version"""
    return get(endpoint=f"archive/id/{id}", params=kwargs, format=format)
@archive.register
def _(id: list, format="json", **kwargs):
    """Retrieve the latest version for a set of identifiers"""
    return post(endpoint=f"archive/id", json={"id": id}, params=kwargs, format=format)

def cafe_genetree_id(id, format="json", **kwargs):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        return get(endpoint=f"cafe/genetree/id/{id}", params=kwargs, format=format)

def cafe_genetree_member_id( id, format="json", **kwargs):
    """Retrieves the cafe tree of the gene tree that contains the gene / transcript / translation stable identifier"""
    return get(endpoint=f"cafe/genetree/member/id/{id}", params=kwargs, format=format)

def cafe_genetree_member_symbol( symbol, species="human", format="json", **kwargs):
    """Retrieves the cafe tree of the gene tree that contains the gene identified by a symbol"""
    return get(endpoint=f"cafe/genetree/member/symbol/{species}/{symbol}", params=kwargs, format=format)

def genetree_id( id, format="json", **kwargs):
    """Retrieves a gene tree for a gene tree stable identifier"""
    return get(endpoint=f"genetree/id/{id}", params=kwargs, format=format)

def genetree_member_id( id, format="json", **kwargs):
    """Retrieves the gene tree that contains the gene / transcript / translation stable identifier"""
    return get(endpoint=f"genetree/member/id/{id}", params=kwargs, format=format)

def genetree_member_symbol( species, symbol, format="json", **kwargs):
    """Retrieves the gene tree that contains the gene identified by a symbol"""
    return get(endpoint=f"genetree/member/symbol/{species}/{symbol}", params=kwargs, format=format)

def alignment_region( species, region, format="json", **kwargs):
        """Retrieves genomic alignments as separate blocks based on a region and species"""
        return get(endpoint=f"alignment/region/{species}/{region}", params=kwargs, format=format)

def homology_id( id, format="json", **kwargs):
    """Retrieves homology information (orthologs) by Ensembl gene id"""
    return get(endpoint=f"homology/id/{id}", params=kwargs, format=format)

def homology_symbol( species, symbol, format="json", **kwargs):
    """Retrieves homology information (orthologs) by symbol"""
    return get(f"homology/symbol/{species}/{symbol}", params=kwargs, format=format)

def xrefs_symbol( species, symbol, format="json", **kwargs):
    """Looks up an external symbol and returns all Ensembl objects linked to it.
    This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference.
    If a gene's transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links)."""
    return get(f"xrefs/symbol/{species}/{symbol}", params=kwargs, format=format)

def xrefs_id( id, format="json", **kwargs):
    """Perform lookups of Ensembl Identifiers and retrieve their external references in other databases"""
    return get(f"xrefs/id/{id}", params=kwargs, format=format)

def xrefs_name(species, name, format="json", **kwargs):
    """Performs a lookup based upon the primary accession or display label of an external reference and returning the information we hold about the entry"""
    return get(f"xrefs/name/{species}/{name}", params=kwargs, format=format)

def info_analysis(species, format="json", **kwargs):
    """List the names of analyses involved in generating Ensembl data."""
    return get(f"info/analysis/{species}", params=kwargs, format=format)

def info_assembly(species, format="json", **kwargs):
    """List the currently available assemblies for a species, along with toplevel sequences, chromosomes and cytogenetic bands."""
    return get(f"info/assembly/{species}", params=kwargs, format=format)

def info_assembly_region_name(species, region_name, format="json", **kwargs):
    """Returns information about the specified toplevel sequence region for the given species."""
    return get(f"info/assembly/{species}/{region_name}", params=kwargs, format=format)

def info_biotypes( species, format="json", **kwargs):
    """List the functional classifications of gene models that Ensembl associates with a particular species.
    Useful for restricting the type of genes/transcripts retrieved by other endpoints."""
    return get(f"info/biotypes/{species}", params=kwargs, format=format)

def info_biotypes_groups( format="json", **kwargs):
    """Without argument the list of available biotype groups is returned.
    With :group argument provided, list the properties of biotypes within that group.
    Object type (gene or transcript) can be provided for filtering."""
    return get(f"info/biotypes/groups", params=kwargs, format=format)

def info_biotypes_name( name, format="json", **kwargs):
    """List the properties of biotypes with a given name. Object type (gene or transcript) can be provided for filtering."""
    return get(f"info/biotypes/name/{name}", params=kwargs, format=format)

def info_compara_methods( format="json", **kwargs):
    """List all compara analyses available (an analysis defines the type of comparative data)."""
    return get(f"info/compara/methods", params=kwargs, format=format)

def info_compara_species_sets( method, format="json", **kwargs):
    """List all collections of species analysed with the specified compara method."""
    return get(f"info/compara/species_sets/{method}", params=kwargs, format=format)

def info_comparas( format="json", **kwargs):
    """Lists all available comparative genomics databases and their data release."""
    return get(f"info/comparas", params=kwargs, format=format)

def info_data( format="json", **kwargs):
    """Shows the data releases available on this REST server."""
    return get(f"info/data", params=kwargs, format=format)

def info_eg_version( format="json", **kwargs):
    """Returns the Ensembl Genomes version of the databases backing this service"""
    return get(f"info/eg_version", params=kwargs, format=format)

def info_external_dbs( species, format="json", **kwargs):
    """Lists all available external sources for a species."""
    return get(f"info/external_dbs/{species}", params=kwargs, format=format)

def info_divisions( format="json", **kwargs):
    """Get list of all Ensembl divisions for which information is available"""
    return get(f"info/divisions", params=kwargs, format=format)

def info_genomes( name, format="json", **kwargs):
    """Find information about a given genome"""
    return get(f"info/genomes/{name}", params=kwargs, format=format)

def info_genomes_accession( accession, format="json", **kwargs):
    """Find information about genomes containing a specified INSDC accession"""
    return get(f"info/genomes/accession/{accession}", params=kwargs, format=format)

def info_genomes_assembly( assembly_id, format="json", **kwargs):
    """Find information about a genome with a specified assembly"""
    return get(f"info/genomes/assembly/{assembly_id}", params=kwargs, format=format)

def info_genomes_division( division, format="json", **kwargs):
    """Find information about all genomes in a given division. May be large for Ensembl Bacteria."""
    return get(f"info/genomes/division/{division}", params=kwargs, format=format)

def info_genomes_taxonomy( taxon_name, format="json", **kwargs):
    """Find information about all genomes beneath a given node of the taxonomy"""
    return get(f"info/genomes/taxonomy/{taxon_name}", params=kwargs, format=format)

def info_ping( format="json", **kwargs):
    """Checks if the service is alive."""
    return get(f"info/ping", params=kwargs, format=format)

def info_rest( format="json", **kwargs):
    """Shows the current version of the Ensembl REST API."""
    return get(f"info/rest", params=kwargs, format=format)

def info_software( format="json", **kwargs):
    """Shows the current version of the Ensembl API used by the REST server."""
    return get(f"info/software", params=kwargs, format=format)

def info_species( format="json", **kwargs):
    """Lists all available species, their aliases, available adaptor groups and data release."""
    return get(f"info/species", params=kwargs, format=format)

def info_variation( species, format="json", **kwargs):
    """List the variation sources used in Ensembl for a species."""
    return get(f"info/variation/{species}", params=kwargs, format=format)

def info_variation_consequence_types( format="json", **kwargs):
    """Lists all variant consequence types."""
    return get(f"info/variation/consequence_types", params=kwargs, format=format)

def info_variation_populations( species, population_name, format="json", **kwargs):
    """List all individuals for a population from a species"""
    return get(f"info/variation/populations/{species}/{population_name}", params=kwargs, format=format)

def info_variation_species( species, format="json", **kwargs):
    """List all populations for a species"""
    return get(f"info/variation/populations/{species}", params=kwargs, format=format)

def ld( species, id, population_name, format="json", **kwargs):
    """Computes and returns LD values between the given variant and all other variants in a window centered around the given variant.
    The window size is set to 500 kb."""
    return get(f"ld/{species}/{id}/{population_name}", params=kwargs, format=format)

def ld_pairwise( species, id1, id2, format="json", **kwargs):
    """Computes and returns LD values between the given variants."""
    return get(f"ld/{species}/pairwise/{id1}/{id2}", params=kwargs, format=format)

def ld_region( species, region, population_name, format="json", **kwargs):
    """Computes and returns LD values between all pairs of variants in the defined region."""
    return get(f"ld/{species}/region/{region}/{population_name}", params=kwargs, format=format)

@singledispatch
def lookup_id( id: str, format="json", **kwargs):
    """Find the species and database for a single identifier e.g. gene, transcript, protein"""
    return get(endpoint=f"lookup/id/{id}", params=kwargs, format=format)

@lookup_id.register
def _( id: list, format="json", **kwargs):
    """Find the species and database for several identifiers. IDs that are not found are returned with no data."""
    return post(endpoint=f"lookup/id", params=kwargs, json={"ids": id}, format=format)

@singledispatch
def lookup_symbol( symbol: str, format="json", species="human", **kwargs):
    """Find the species and database for a symbol in a linked external database"""
    return get(f"lookup/symbol/{species}/{symbol}", params=kwargs, format=format)

@lookup_symbol.register
def _( symbol: list, species="human", format="json", **kwargs):
    """Find the species and database for a set of symbols in a linked external database. Unknown symbols are omitted from the response."""
    return post(f"lookup/symbol/{species}", params=kwargs, json={"symbols": symbol}, format=format)

def map_cdna( id, region, format="json", **kwargs):
    """Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
    return get(f"map/cdna/{id}/{region}", params=kwargs, format=format)

def map_cds( id, region, format="json", **kwargs):
    """Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
    return get(f"map/cds/{id}/{region}", params=kwargs, format=format)

def map_assembly( species, asm_one, region, asm_two, format="json", **kwargs):
    """Convert the co-ordinates of one assembly to another"""
    return get(f"map/{species}/{asm_one}/{region}/{asm_two}", params=kwargs, format=format)

def map_translation( id, region, format="json", **kwargs):
    """Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API."""
    return get(f"map/translation/{id}/{region}", params=kwargs, format=format)

def ontology_ancestors( id, format="json", **kwargs):
    """Reconstruct the entire ancestry of a term from is_a and part_of relationships"""
    return get(f"ontology/ancestors/{id}", params=kwargs, format=format)

def ontology_ancestors_chart( id, format="json", **kwargs):
    """Reconstruct the entire ancestry of a term from is_a and part_of relationships"""
    return get(f"ontology/ancestors/chart/{id}", params=kwargs, format=format)

def ontology_descendants( id, format="json", **kwargs):
    """Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier"""
    return get(f"ontology/descendants/{id}", params=kwargs, format=format)

def ontology_id( id, format="json", **kwargs):
    """Search for an ontological term by its namespaced identifier"""
    return get(f"ontology/id/{id}", params=kwargs, format=format)

def ontology_name( name, format="json", **kwargs):
    """Search for a list of ontological terms by their name"""
    return get(f"ontology/name/{name}", params=kwargs, format=format)

def taxonomy_classification( id, format="json", **kwargs):
    """Return the taxonomic classification of a taxon node"""
    return get(f"taxonomy/classification/{id}", params=kwargs, format=format)

def taxonomy_id( id, format="json", **kwargs):
    """Search for a taxonomic term by its identifier or name"""
    return get(f"taxonomy/id/{id}", params=kwargs, format=format)

def taxonomy_name( name, format="json", **kwargs):
    """Search for a taxonomic id by a non-scientific name"""
    return get(f"taxonomy/name/{name}", params=kwargs, format=format)

def overlap_id( id, format="json", **kwargs):
    """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a region defined by the given identifier."""
    return get(f"overlap/id/{id}", params=kwargs, format=format)

def overlap_region( species, region, format="json", **kwargs):
    """Retrieves features (e.g. genes, transcripts, variants and more) that overlap a given region."""
    return get(f"overlap/region/{species}/{region}", params=kwargs, format=format)

def overlap_translation( id, format="json", **kwargs):
    """Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variants)."""
    return get(f"overlap/translation/{id}", params=kwargs, format=format)

def phenotype_accession( species, accession, format="json", **kwargs):
    """Return phenotype annotations for genomic features given a phenotype ontology accession"""
    return get(f"phenotype/accession/{species}/{accession}", params=kwargs, format=format)

def phenotype_gene( species, gene, format="json", **kwargs):
    """Return phenotype annotations for a given gene."""
    return get(f"phenotype/gene/{species}/{gene}", params=kwargs, format=format)

def phenotype_region( species, region, format="json", **kwargs):
    """Return phenotype annotations that overlap a given genomic region."""
    return get(f"phenotype/region/{species}/{region}", params=kwargs, format=format)

def phenotype_term( species, term, format="json", **kwargs):
    """Return phenotype annotations for genomic features given a phenotype ontology term"""
    return get(f"phenotype/term/{species}/{term}", params=kwargs, format=format)

def regulatory_microarray_vendor( species, microarray, vendor, format="json", **kwargs):
    """Returns information about a specific microarray"""
    return get(f"regulatory/species/{species}/microarray/{microarray}/vendor/{vendor}", params=kwargs, format=format)

def regulatory_species( species, format="json", **kwargs):
    """Returns information about all epigenomes available for the given species"""
    return get(f"regulatory/species/{species}/epigenome", params=kwargs, format=format)

def species_binding_matrix( species, binding_matrix_stable_id, format="json", **kwargs):
    """Return the specified binding matrix"""
    return get(f"species/{species}/binding_matrix/{binding_matrix_stable_id}", params=kwargs, format=format)

def regulatory_microarray( species, format="json", **kwargs):
    """Returns information about all microarrays available for the given species"""
    return get(f"regulatory/species/{species}/microarray", params=kwargs, format=format)

def regulatory_probe( species, microarray, probe, format="json", **kwargs):
    """Returns information about a specific probe from a microarray"""
    return get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe}", params=kwargs, format=format)

def regulatory_probe_set( species, microarray, probe_set, format="json", **kwargs):
    """Returns information about a specific probe_set from a microarray"""
    return get(f"regulatory/species/{species}/microarray/{microarray}/probe/{probe_set}", params=kwargs, format=format)

def regulatory_id( species, id, format="json", **kwargs):
    """Returns a RegulatoryFeature given its stable ID (e.g. ENSR00000082023)"""
    return get(f"regulatory/species/{species}/id/{id}", params=kwargs, format=format)

@singledispatch
def sequence_id( id: str, format="json", **kwargs):
    """Request multiple types of sequence by stable identifier. Supports feature masking and expand options."""
    return get(f"sequence/id/{id}", params=kwargs, format=format)

@sequence_id.register
def _( id: list, format="json", **kwargs):
    """Request multiple types of sequence by a stable identifier list."""
    return post(f"sequence/id", json={'ids': id}, params=kwargs, format=format)

@singledispatch
def sequence_region( region: str, species, format="json", **kwargs):
    """Returns the genomic sequence of the specified region of the given species. Supports feature masking and expand options."""
    return get(f"sequence/region/{species}/{region}", params=kwargs, format=format)

@sequence_region.register
def _( region: list, species, format="json", **kwargs):
    """Request multiple types of sequence by a list of regions."""
    return post(f"sequence/region/{species}", json={'region': region}, params=kwargs, format=format)

def transcript_haplotypes( species, id, format="json", **kwargs):
    """Computes observed transcript haplotype sequences based on phased genotype data"""
    return get(f"transcript_haplotypes/{species}/{id}", params=kwargs, format=format)

def ga4gh_beacon( format="json", **kwargs):
    """Return Beacon information"""
    return get(f"ga4gh/beacon", params=kwargs, format=format)

@singledispatch
def ga4gh_beacon_query( query: str, format="json", **kwargs):
    """Return the Beacon response for allele information"""
    return get(f"ga4gh/beacon/{query}", params=kwargs, format=format)

@ga4gh_beacon_query.register
def _( query: list, format="json", **kwargs):
    """Return the Beacon response for allele information"""
    return post(f"ga4gh/beacon", json={"query": query}, params=kwargs, format=format)

def ga4gh_features( id, format="json", **kwargs):
    """Return the GA4GH record for a specific sequence feature given its identifier"""
    return get(f"ga4gh/features/{id}", params=kwargs, format=format)

def ga4gh_features_search( end, referenceName, start, format="json", **kwargs):
    """Return a list of sequence annotation features in GA4GH format"""
    return post(f"ga4gh/features/search", json=dict(end=end, referenceName=referenceName, start=start, **kwargs), params={}, format=format)

def ga4gh_callsets_search( variantSetId, format="json", **kwargs):
    """Return a list of sets of genotype calls for specific samples in GA4GH format"""
    return post(f"ga4gh/callsets/search", json=dict(variantSetId=variantSetId, **kwargs), params={}, format=format)

def ga4gh_callsets( id, format="json", **kwargs):
    """Return the GA4GH record for a specific CallSet given its identifier"""
    return get(f"ga4gh/callsets/{id}", params=kwargs, format=format)

def ga4gh_datasets_search( format="json", **kwargs):
    """Return a list of datasets in GA4GH format"""
    return post(f"ga4gh/datasets/search", json=kwargs, params={}, format=format)

def ga4gh_datasets( id, format="json", **kwargs):
    """Return the GA4GH record for a specific dataset given its identifier"""
    return get(f"ga4gh/datasets/{id}", params=kwargs, format=format)

def ga4gh_featuresets_search( datasetId, format="json", **kwargs):
    """Return a list of feature sets in GA4GH format"""
    return post(f"ga4gh/featuresets/search", json=dict(datasetId=datasetId, **kwargs), params={}, format=format)

def ga4gh_featuresets( id, format="json", **kwargs):
    """Return the GA4GH record for a specific featureSet given its identifier"""
    return get(f"ga4gh_featuresets/{id}", params=kwargs, format=format)

def ga4gh_variants( id, format="json", **kwargs):
    """Return the GA4GH record for a specific variant given its identifier."""
    return get(f"ga4gh/variants/{id}", params=kwargs, format=format)

def ga4gh_variants_search( end, referenceName, start, variantSetId, format="json", **kwargs):
    """Return variant call information in GA4GH format for a region on a reference sequence"""
    return post(f"ga4gh/variants/search", json=dict(end=end, referenceName=referenceName, start=start, variantSetId=variantSetId, **kwargs), params={}, format=format)

def ga4gh_variantannotations_search( variantAnnotationSetId, format="json", **kwargs):
    """Return variant annotation information in GA4GH format for a region on a reference sequence"""
    return post(f"ga4gh/variantannotations/search", json=dict(variantAnnotationSetId=variantAnnotationSetId, **kwargs), params={}, format=format)

def ga4gh_variantsets_search( datasetId, format="json", **kwargs):
    """Return a list of variant sets in GA4GH format"""
    return post(f"ga4gh/variantsets/search", json=dict(datasetId=datasetId, **kwargs), params={}, format=format)

def ga4gh_variantsets( id, format="json", **kwargs):
    """Return the GA4GH record for a specific VariantSet given its identifier"""
    return get(f"ga4gh/variantsets/{id}", params=kwargs, format=format)

def ga4gh_references_search( referenceSetId, format="json", **kwargs):
    """Return a list of reference sequences in GA4GH format"""
    return post(f"ga4gh/references/search", json=dict(referenceSetId=referenceSetId, **kwargs), params={}, format=format)

def ga4gh_references( id, format="json", **kwargs):
    """Return data for a specific reference in GA4GH format by id"""
    return get(f"ga4gh/references/{id}", params=kwargs, format=format)

def ga4gh_referencesets_search( referenceSetId, format="json", **kwargs):
    """Return a list of reference sets in GA4GH format"""
    return post(f"ga4gh/referencesets/search", json=dict(referenceSetId=referenceSetId, **kwargs), params={}, format=format)

def ga4gh_referencesets( id, format="json", **kwargs):
    """Return data for a specific reference set in GA4GH format"""
    return get(f"ga4gh/referencesets/{id}", params=kwargs, format=format)

def ga4gh_variantannotationsets_search( variantSetId, format="json", **kwargs):
    """Return a list of annotation sets in GA4GH format"""
    return post(f"ga4gh/variantannotationsets/search", json=dict(variantSetId=variantSetId, **kwargs), params={}, format=format)

def ga4gh_variantannotationsets( id, format="json", **kwargs):
    """Return meta data for a specific annotation set in GA4GH format"""
    return get(f"ga4gh/variantannotationsets/{id}", params=kwargs, format=format)

@singledispatch
def variant_recoder( id: str, species='human', format="json", **kwargs):
    """Translate a variant identifier, HGVS notation or genomic SPDI notation to all possible variant IDs, HGVS and genomic SPDI"""
    return get(endpoint=f"variant_recoder/{species}/{id}", params=kwargs, format=format)

@variant_recoder.register
def _( id: list, species='human', format="json", **kwargs):
    """Translate a list of variant identifiers, HGVS notations or genomic SPDI notations to all possible variant IDs, HGVS and genomic SPDI"""
    return post(endpoint=f"variant_recoder/{species}", params=kwargs, json={"ids": id}, format=format)

@singledispatch
def variation( id: str, species='human', format="json", **kwargs):
    """Uses a variant identifier (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
    return get(endpoint=f"variation/{species}/{id}", params=kwargs, format=format)

@variation.register
def _( id: list, species='human', format="json", **kwargs):
    """Uses a list of variant identifiers (e.g. rsID) to return the variation features including optional genotype, phenotype and population data"""
    return post(endpoint=f"variation/{species}", params=kwargs, json={"ids": id}, format=format)

def variation_pmcid( pmcid, species='human', format="json", **kwargs):
    """Fetch variants by publication using PubMed Central reference number (PMCID)"""
    return get(endpoint=f"variation/{species}/pmcid/{pmcid}", params=kwargs, format=format)

def variation_pmid( pmid, species='human', format="json", **kwargs):
    """Fetch variants by publication using PubMed reference number (PMID)"""
    return get(endpoint=f"variation/{species}/pmid/{pmid}", params=kwargs, format=format)

@singledispatch
def vep_hgvs( hgvs: str, species='human', format="json", **kwargs):
    """Fetch variant consequences based on a HGVS notation"""
    return get(endpoint=f"vep/{species}/hgvs/{hgvs}", params=kwargs, format=format)

@vep_hgvs.register
def _( hgvs: list, species='human', format="json", **kwargs):
    """Fetch variant consequences for multiple HGVS notations"""
    return post(endpoint=f"vep/{species}/hgvs", params=kwargs, json={"hgvs_notations": hgvs}, format=format)

@singledispatch
def vep_id( id: str, species='human', format="json", **kwargs):
    """Fetch variant consequences based on a variant identifier"""
    return get(endpoint=f"vep/{species}/id/{id}", params=kwargs, format=format)

@vep_id.register
def _( id: list, species='human', format="json", **kwargs):
    """Fetch variant consequences for multiple ids"""
    return post(endpoint=f"vep/{species}/id", params=kwargs, json={"ids": id}, format=format)

@singledispatch
def vep_region( region: str, allele, species='human', format="json", **kwargs):
    """Fetch variant consequences based on a region"""
    return get(endpoint=f"vep/{species}/region/{region}/{allele}", params=kwargs, format=format)

@vep_region.register
def _( region: list, species='human', format="json", **kwargs):
    """Fetch variant consequences for multiple regions"""
    return post(endpoint=f"vep/{species}/region", params=kwargs, json={"variants": region}, format=format)

