import argparse
import pprint
from functools import singledispatch

import requests


@singledispatch
def _variant_recoder(id: str, species='human', fields=None, var_synonyms=None, vcf_string=None, format='json'):
    response = requests.get(
        f"https://rest.ensembl.org/variant_recoder/{species}/{id}", headers={"Content-Type": "application/json"}, params=dict(fields=fields, var_synonyms=var_synonyms, vcf_string=vcf_string, format=format))
    return response.json()


@_variant_recoder.register
def _(id: list, species='human', fields=None, var_synonyms=None, vcf_string=None, format='json'):
    response = requests.post(
        f"https://rest.ensembl.org/variant_recoder/{species}", headers={"Content-Type": "application/json"}, params=dict(fields=fields, var_synonyms=var_synonyms, vcf_string=vcf_string, format=format), json={"ids": id})
    return response.json()


@singledispatch
def _variation(id: str, species='human', pops=None, genotypes=None, genotyping_chips=None, phenotypes=None, population_genotypes=None, format='json'):
    response = requests.get(
        f"https://rest.ensembl.org/variation/{species}/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format, pops=pops, genotypes=genotypes, genotyping_chips=genotyping_chips, phenotypes=phenotypes, population_genotypes=population_genotypes))
    return response.json()


@_variation.register
def _(id: list, species='human', pops=None, genotypes=None, genotyping_chips=None, phenotypes=None, population_genotypes=None, format='json'):
    response = requests.post(
        f"https://rest.ensembl.org/variation/{species}", headers={"Content-Type": "application/json"}, params=dict(format=format, pops=pops, genotypes=genotypes, genotyping_chips=genotyping_chips, phenotypes=phenotypes, population_genotypes=population_genotypes), json={"ids": id})
    return response.json()

def _variation_pmcid(pmcid: str, species='human',format='json'):
    response = requests.get(
        f"https://rest.ensembl.org/variation/{species}/pmcid/{pmcid}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _variation_pmid(pmid: str, species='human',format='json'):
    response = requests.get(
        f"https://rest.ensembl.org/variation/{species}/pmid/{pmid}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()


@singledispatch
def _archive(id: str, format='json'):
    """Uses the given identifier to return its latest version"""
    response = requests.get(
        f"https://rest.ensembl.org/archive/id/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()


@_archive.register
def _(id: list, format='json'):
    """Retrieve the latest version for a set of identifiers"""
    response = requests.post(f"https://rest.ensembl.org/archive/id",
                             headers={"Content-Type": "application/json"}, json={"id": id}, params=dict(format=format))
    return response.json()

def _cafe_genetree_id(id:str, compara=None, nh_format=None,format='json'):
    """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
    response =requests.get(f"https://rest.ensembl.org/cafe/genetree/id/{id}", headers={"Content-Type": "application/json"}, params=dict(compara=compara, nh_format=nh_format,format=format))
    return response.json()

def _cafe_genetree_member(id: str, compara=None, db_type=None, nh_format=None, object_type=None, species=None,format='json'):
    """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
    response = requests.get(f"https://rest.ensembl.org/cafe/genetree/member/id/{id}", headers={"Content-Type": "application/json"}, params=dict(
        compara=compara, db_type=db_type, nh_format=nh_format, object_type=object_type, species=species,format=format))
    return response.json()

def _cafe_genetree_member_symbol(symbol:str,species='human', compara=None, db_type=None,external_db=None,nh_format=None,object_type=None,format='json'):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/cafe/genetree/member/symbol/{species}/{symbol}", headers={"Content-Type": "application/json"}, 
                               params=dict(compara=compara, db_type=db_type,external_db=external_db,nh_format=nh_format,object_type=object_type,format=format))
        return response.json()
def _genetree_id(id:str, aligned=None,cigar_line=None,clusterset_id=None,compara=None,nh_format=None,prune_species=None,prune_taxon=None,sequence=None,format="json"):
    """Retrieves a gene tree for a gene tree stable identifier"""
    response =requests.get(f"https://rest.ensembl.org/genetree/id/{id}",headers={"Content-Type": "application/json"}, 
                            params=dict(aligned=aligned,cigar_line=cigar_line,clusterset_id=clusterset_id,compara=compara,nh_format=nh_format,
                                        prune_species=prune_species,prune_taxon=prune_taxon,sequence=sequence,format=format))
    return response.json()

def _genetree_member_id(id:str, aligned=None,cigar_line=None,clusterset_id=None,compara=None,db_type=None,nh_format=None,object_type=None,
                        prune_species=None,prune_taxon=None,sequence=None,species=None,format="json"):
    """Retrieves a gene tree for a gene tree stable identifier"""
    response =requests.get(f"https://rest.ensembl.org/genetree/member/id/{id}",headers={"Content-Type": "application/json"}, 
                            params=dict(aligned=aligned,cigar_line=cigar_line,clusterset_id=clusterset_id,compara=compara,db_type=db_type,nh_format=nh_format,
                                        object_type=object_type,prune_species=prune_species,prune_taxon=prune_taxon,sequence=sequence,species=species,format=format))
    return response.json()


def _genetree_member_symbol(symbol:str,species='homo_sapiens',aligned=None,cigar_line=None,clusterset_id=None,compara=None,db_type=None,external_db=None,nh_format=None,object_type=None,
                        prune_species=None,prune_taxon=None,sequence=None,format="json"):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/genetree/member/symbol/{species}/{symbol}", headers={"Content-Type": "application/json"}, 
                               params=dict(aligned=aligned,cigar_line=cigar_line,clusterset_id=clusterset_id,compara=compara,db_type=db_type,nh_format=nh_format,
                                        object_type=object_type,external_db=external_db,prune_species=prune_species,prune_taxon=prune_taxon,sequence=sequence,format=format))
        return response.json()

def _alignment_region(region:str,species='homo_sapiens',aligned=None,compact=None,compara=None,display_species_set=None,mask=None,method=None,species_set=None,species_set_group=None,format="json"):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/alignment/region/{species}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(aligned=aligned,compact=compact,compara=compara,display_species_set=display_species_set,mask=mask,method=method,species_set=species_set,
                                           species_set_group=species_set_group,format=format))
        return response.json()


def _homology_id(id:str, aligned=None,cigar_line=None,compara=None,sequence=None,target_species=None,target_taxon=None,type=None,format=None):
    """Retrieves a gene tree for a gene tree stable identifier"""
    response =requests.get(f"https://rest.ensembl.org/homology/id/{id}",headers={"Content-Type": "application/json"}, 
                            params=dict(aligned=aligned,cigar_line=cigar_line,compara=compara,sequence=sequence,target_species=target_species,target_taxon=target_taxon,
                                        type=type,format=format))
    return response.json()

def _homology_symbol(symbol:str,species='homo_sapiens',aligned=None,cigar_line=None,compara=None,external_db=None,format=None,sequence=None,
                   target_species=None,target_taxon=None,type=None):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/homology/symbol/{species}/{symbol}", headers={"Content-Type": "application/json"}, 
                               params=dict(aligned=aligned,cigar_line=cigar_line,compara=compara,external_db=external_db,
                                           format=format,sequence=sequence,target_species=target_species,target_taxon=target_taxon,type=type))
        return response.json()

def _xrefs_symbol(symbol:str,species='homo_sapiens',db_type=None,external_db=None,object_type=None,format="json"):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/xrefs/symbol/{species}/{symbol}", headers={"Content-Type": "application/json"}, 
                               params=dict(db_type=db_type,external_db=external_db,object_type=object_type,format=format))
        return response.json()
    

def _xrefs_id(id:str,all_levels=None,db_type=None,external_db=None,object_type=None,species=None,format="json"):
    """Retrieves a gene tree for a gene tree stable identifier"""
    response =requests.get(f"https://rest.ensembl.org/xrefs/id/{id}",headers={"Content-Type": "application/json"}, 
                            params=dict(all_levels=all_levels,db_type=db_type,external_db=external_db,object_type=object_type,species=species,format=format))
    return response.json()
def _xrefs_name(name:str,species='homo_sapiens',db_type=None,external_db=None,format="json"):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/xrefs/name/{species}/{name}", headers={"Content-Type": "application/json"}, 
                               params=dict(db_type=db_type,external_db=external_db,format=format))
        return response.json()

def _info_analysis(species='homo_sapiens',format="json"):
    response =requests.get(f"https://rest.ensembl.org/info/analysis/{species}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_assembly(species='homo_sapiens',bands=None,synonyms=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/assembly/{species}", headers={"Content-Type": "application/json"}, 
                               params=dict(bands=bands,synonyms=synonyms,format=format))
    return response.json()

def _info_assembly_region_name(region_name:str,species='homo_sapiens',bands=None,synonyms=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/assembly/{species}/{region_name}", headers={"Content-Type": "application/json"}, 
                               params=dict(bands=bands,synonyms=synonyms,format=format))
    return response.json()


def _info_biotypes(species='homo_sapiens',format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/biotypes/{species}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()


def _info_biotypes_group(group=None,object_type=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org//info/biotypes/groups", headers={"Content-Type": "application/json"}, 
                               params=dict(group=group,object_type=object_type,format=format))
    return response.json()

def _info_biotypes_name(name:str,object_type=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/biotypes/name/{name}", headers={"Content-Type": "application/json"}, 
                               params=dict(object_type=object_type,format=format))
    return response.json()

def _info_compara_methods(cla=None,compara=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/compara/methods", headers={"Content-Type": "application/json"}, 
                               params=dict(cla=cla,compara=compara,format=format))
    return response.json()

def _info_compara_species_sets(method:str,compara=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/compara/species_sets/{method}", headers={"Content-Type": "application/json"}, 
                               params=dict(compara=compara,format=format))
    return response.json()

def _info_comparas(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/comparas", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_data(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/data", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_eg_version(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/eg_version", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_external_dbs(species='homo_sapiens',feature=None,filter=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/external_dbs/{species}", headers={"Content-Type": "application/json"}, 
                               params=dict(feature=feature,filter=filter,format=format))
    return response.json()

def _info_divisions(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/divisions", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_genomes(name:str,expand=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org//info/genomes/{name}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()

def _info_genomes_accession(accession:str,expand=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/genomes/accession/{accession}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()

def _info_genomes_assembly(assembly_id:str,expand=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/genomes/assembly/{assembly_id}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()

def _info_genomes_division(division:str,expand=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/genomes/division/{division}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()
# Homo sapiens引用时空格替换为'_'
def _info_genomes_taxonomy(taxon_name:str,expand=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/genomes/taxonomy/{taxon_name}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()

def _info_ping(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/ping", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_rest(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/rest", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_software(format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/software", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _info_species(division=None,hide_strain_info=None,strain_collection=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/species", headers={"Content-Type": "application/json"}, 
                               params=dict(division=division,hide_strain_info=hide_strain_info,strain_collection=strain_collection,format=format))
    return response.json()

def _info_variation(species='human',filter=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/species", headers={"Content-Type": "application/json"}, 
                               params=dict(filter=filter,hformat=format))
    return response.json()

def _info_variation_consequence_types(rank=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/variation/consequence_types", headers={"Content-Type": "application/json"}, 
                               params=dict(rank=rank,format=format))
    return response.json()

def _info_variation_populations(population_name:str,species='human',format='json'):
    response =requests.get(f"https://rest.ensembl.org/info/variation/populations/{species}/{population_name}", headers={"Content-Type": "application/json"}, 
                               params=dict(species=species,format=format))
    return response.json()

def _info_variation_species(species='homo_sapiens',format='json',filter=None):
    response =requests.get(f"https://rest.ensembl.org/info/variation/populations/{species}", headers={"Content-Type": "application/json"}, 
                               params=dict(species='homo_sapiens',filter=filter,format=format))
    return response.json()

def _ld(id:str,population_name:str,species='human',format='json',attribs=None,callback=None,d_prime=None,r2=None,window_size=None):
    response =requests.get(f"https://rest.ensembl.org/ld/{species}/{id}/{population_name}", headers={"Content-Type": "application/json"}, 
                               params=dict(species='homo_sapiens',attribs=attribs,callback=callback,d_prime=d_prime,r2=r2,window_size=window_size,format=format))
    return response.json()

def _ld_pairwise(id1:str,id2:str,species='human',d_prime=None,population_name=None,r2=None,format='json',):
    response =requests.get(f"https://rest.ensembl.org/ld/{species}/pairwise/{id1}/{id2}", headers={"Content-Type": "application/json"}, 
                               params=dict(d_prime=d_prime,population_name=population_name,r2=r2,format=format))
    return response.json()

def _ld_region(population_name:str,region:str,species='human',d_prime=None,r2=None,format='json',):
    response =requests.get(f"https://rest.ensembl.org/ld/{species}/region/{population_name}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(d_prime=d_prime,r2=r2,format=format))
    return response.json()

@singledispatch
def _lookup_id(id:str,db_type=None,expand=None,mane=None,phenotypes=None,species=None,utr=None,format=None):
    response =requests.get(f"https://rest.ensembl.org//lookup/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(db_type=db_type,expand=expand,mane=mane,phenotypes=phenotypes,
                               species=species,utr=utr,format=format))
    return response.json()
@ _lookup_id.register
def _(id: list,db_type=None,expand=None,mane=None,phenotypes=None,species=None,utr=None,format=None):
    response = requests.post(
        f"https://rest.ensembl.org/lookup/id", headers={"Content-Type": "application/json"}, json={"ids": id},
        params=dict(db_type=db_type,expand=expand,mane=mane,phenotypes=phenotypes,
                               species=species,utr=utr,format=format))
    return response.json()

@singledispatch
def _lookup_symbol(symbol:str,species='human',expand=None,format=None):
    response =requests.get(f"https://rest.ensembl.org//lookup/symbol/{species}/{symbol}", headers={"Content-Type": "application/json"}, 
                               params=dict(expand=expand,format=format))
    return response.json()
@ _lookup_symbol.register
def _(symbol: list,species='human',expand=None,format=None):
    response = requests.post(
        f"https://rest.ensembl.org/lookup/symbol", headers={"Content-Type": "application/json"}, json={"symbol": symbol},
        params=dict(expand=expand,format=format))
    return response.json()

def _map_cdna(id:str,region:str,include_original_region=None,species=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/map/cdna/{id}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(include_original_region=include_original_region,species=species,format=format))
    return response.json()

def _map_cds(id:str,region:str,include_original_region=None,species=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/map/cds/{id}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(include_original_region=include_original_region,species=species,format=format))
    return response.json()

def _map_assembly(asm_one:str,asm_two:str,region:str,species='human',coord_system=None,target_coord_system=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/map/{species}/{asm_one}/{asm_two}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(coord_system=coord_system,target_coord_system=target_coord_system,format=format))
    return response.json()

def _map_translation(id:str,region:str,species=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/map/translation/{id}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(species=species,format=format))
    return response.json()

def _ontology_ancestors(id:str,ontology=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ontology/ancestors/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(ontology=ontology,format=format))
    return response.json()

def _ontology_ancestors_chart(id:str,ontology=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ontology/ancestors/chart/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(ontology=ontology,format=format))
    return response.json()

def _ontology_descendants(id:str,closest_term=None,ontology=None,subset=None,zero_distance=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ontology/descendants/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(closest_term=closest_term,ontology=ontology,subset=subset,zero_distance=zero_distance,format=format))
    return response.json()

def _ontology_id(id:str,relation=None,simple=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ontology/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(relation=relation,simple=simple,format=format))
    return response.json()

def _ontology_name(name:str,ontology=None,relation=None,simple=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ontology/name/{name}", headers={"Content-Type": "application/json"}, 
                               params=dict(ontology=ontology,relation=relation,simple=simple,format=format))
    return response.json()

def _taxonomy_classification(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/taxonomy/classification/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _taxonomy_id(id:str,simple=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/taxonomy/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(simple=simple,format=format))
    return response.json()

def _taxonomy_name(name:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/taxonomy/name/{name}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _overlap_id(id:str,feature,biotype=None,db_type=None,logic_name=None,misc_set=None,object_type=None,so_term=None,species=None,
                        species_set=None,variant_set=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/overlap/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(feature=feature,biotype=biotype,db_type=db_type,logic_name=logic_name,misc_set=misc_set,object_type=object_type,so_term=so_term,species=species,
                                           species_set=species_set,variant_set=variant_set,format=format))
    return response.json()

def _overlap_region(region:str,feature,species='homo_sapiens',biotype=None,db_type=None,logic_name=None,misc_set=None,so_term=None,species_set=None,
                    trim_downstream=None,trim_upstream=None,variant_set=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org//overlap/region/{species}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(feature=feature,biotype=biotype,db_type=db_type,logic_name=logic_name,misc_set=misc_set,so_term=so_term,
                                           species_set=species_set,trim_downstream=trim_downstream,trim_upstream=trim_upstream,variant_set=variant_set,format=format))
    return response.json()
    
def _overlap_translation(id:str,db_type=None,feature=None,so_term=None,species=None,type=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/overlap/translation/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(db_type=db_type,feature=feature,so_term=so_term,species=species,type=type,format=format))
    return response.json()

def _phenotype_accession(accession:str,species='homo_sapiens',include_children=None,include_pubmed_id=None,include_review_status=None,source=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/phenotype/accession/homo_sapiens/{accession}", headers={"Content-Type": "application/json"}, 
                               params=dict(species=species,include_children=include_children,include_pubmed_id=include_pubmed_id,include_review_status=include_review_status,source=source,format=format))
    return response.json()

def _phenotype_gene(gene:str,species='homo_sapiens',include_associated=None,include_overlap=None,include_pubmed_id=None,include_review_status=None,include_submitter=None,non_specified=None,trait=None,tumour=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/phenotype/gene/{gene}", headers={"Content-Type": "application/json"}, 
                               params=dict(species=species,include_associated=include_associated,include_overlap=include_overlap,include_pubmed_id=include_pubmed_id,include_review_status=include_review_status,include_submitter=include_submitter,non_specified=non_specified,
                                           trait=trait,tumour=tumour,format=format))
    return response.json()

def _phenotype_region(region:str,species='homo_sapiens',feature_type=None,include_pubmed_id=None,include_review_status=None,include_submitter=None,non_specified=None,only_phenotypes=None,trait=None,tumour=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/phenotype/region/{species}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(species=species,feature_type=feature_type,include_pubmed_id=include_pubmed_id,include_review_status=include_review_status,include_submitter=include_submitter,non_specified=non_specified,only_phenotypes=only_phenotypes,trait=trait,tumour=tumour,format=format))
    return response.json()

def _phenotype_term(term:str,species='homo_sapiens',include_children=None,include_pubmed_id=None,include_review_status=None,source=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/phenotype/term/{species}/{term}", headers={"Content-Type": "application/json"}, 
                               params=dict(include_children=include_children,include_pubmed_id=include_pubmed_id,include_review_status=include_review_status,source=source,format=format))
    return response.json()

def _regulatory_microarray_vendor(microarray:str,vendor:str,species='homo_sapiens',format='json'):
    response =requests.get(f"https://rest.ensembl.org/regulatory/species/{species}/microarray/{microarray}/vendor/{vendor}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _regulatory_species(species='homo_sapiens',format='json'):
    response =requests.get(f"https://rest.ensembl.org/regulatory/species/{species}/epigenome", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _species_binding_matrix(binding_matrix:str,species='homo_sapiens',unit=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/species/{species}/binding_matrix/{binding_matrix}", headers={"Content-Type": "application/json"}, 
                               params=dict(unit=unit,format=format))
    return response.json()

def _regulatory_microarray(species='homo_sapiens',format='json'):
    response =requests.get(f"https://rest.ensembl.org//regulatory/species/{species}/microarray", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _regulatory_probe(microarray:str,probe:str,species='homo_sapiens',gene=None,transcripts=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/regulatory/species/{species}/microarray/{microarray}/probe/{probe}", headers={"Content-Type": "application/json"}, 
                               params=dict(gene=gene,transcripts=transcripts,format=format))
    return response.json()

def _regulatory_probe_set(microarray:str,probe_set:str,species='homo_sapiens',gene=None,transcripts=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/regulatory/species/{species}/microarray/{microarray}/probe_set/{probe_set}", headers={"Content-Type": "application/json"}, 
                               params=dict(gene=gene,transcripts=transcripts,format=format))
    return response.json()

def _regulatory_id(id:str,species='homo_sapiens',activity=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/regulatory/species/{species}/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(activity=activity,format=format))
    return response.json()

@singledispatch
def _sequence_id(id:str,db_type=None,end=None,expand_3prime=None,expand_5prime=None,mask=None,mask_feature=None,multiple_sequences=None,object_type=None,species=None,start=None,type=None,format=None):
    response =requests.get(f"https://rest.ensembl.org/sequence/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(db_type=db_type,end=end,expand_3prime=expand_3prime,expand_5prime=expand_5prime,mask=mask,mask_feature=mask_feature,multiple_sequences=multiple_sequences,object_type=object_type,species=species,start=start,type=type,format=format))
    return response.json()

@_sequence_id.register
def _(id:list,db_type=None,end=None,expand_3prime=None,expand_5prime=None,mask=None,mask_feature=None,multiple_sequences=None,object_type=None,species=None,start=None,type=None,format=None):
    response =requests.post(f"https://rest.ensembl.org/sequence/id/", headers={"Content-Type": "application/json"}, json={'ids': id},
                               params=dict(db_type=db_type,end=end,expand_3prime=expand_3prime,expand_5prime=expand_5prime,mask=mask,mask_feature=mask_feature,multiple_sequences=multiple_sequences,object_type=object_type,species=species,start=start,type=type,format=format))
    return response.json()

@singledispatch
def _sequence_region(region:str,species='human',coord_system=None,coord_system_version=None,expand_3prime=None,expand_5prime=None,mask=None,mask_feature=None,format=None):
    response =requests.get(f"https://rest.ensembl.org/sequence/region/{species}/{region}", headers={"Content-Type": "application/json"}, 
                               params=dict(coord_system=coord_system,coord_system_version=coord_system_version,expand_3prime=expand_3prime,expand_5prime=expand_5prime,mask=mask,mask_feature=mask_feature,format=format))
    return response.json()

@_sequence_region.register
def _(region:list,species='human',coord_system=None,coord_system_version=None,expand_3prime=None,expand_5prime=None,mask=None,mask_feature=None,format=None):
    response =requests.post(f"https://rest.ensembl.org/sequence/region/{species}/", headers={"Content-Type": "application/json"}, json={'regions': region},
                               params=dict(coord_system=coord_system,coord_system_version=coord_system_version,expand_3prime=expand_3prime,expand_5prime=expand_5prime,mask=mask,mask_feature=mask_feature,format=format))
    return response.json()

def _transcript_haplotypes(id:str,species='homo_sapiens',aligned_sequences=None,samples=None,sequence=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/transcript_haplotypes/{species}/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(aligned_sequences=aligned_sequences,samples=samples,sequence=sequence,format=format))
    return response.json()

def _transcript_haplotypes(hgvs_notation:str,species='homo_sapiens',aligned_sequences=None,samples=None,sequence=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/transcript_haplotypes/{species}/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(aligned_sequences=aligned_sequences,samples=samples,sequence=sequence,format=format))
    return response.json()

@singledispatch
def _vep_hgvs(hgvs_notation:str,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/vep/{species}/hgvs/{hgvs_notation}", headers={"Content-Type": "application/json"}, 
                               params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,ambiguous_hgvs=ambiguous_hgvs,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
    return response.json()

@_vep_hgvs.register
def _(hgvs_notation:list,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/vep/{species}/hgvs/", headers={"Content-Type": "application/json"}, json={'hgvs_notations': hgvs_notation},
                               params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,ambiguous_hgvs=ambiguous_hgvs,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
    return response.json()

@singledispatch
def _vep_id(id:str,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/vep/{species}/id/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
    return response.json()

@_vep_id.register
def _(id:list,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/vep/{species}/id/", headers={"Content-Type": "application/json"}, json={'ids':id},
                               params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
    return response.json()


def _vep_region_get(allele:str,region:str,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
    response =requests.get(f"https://rest.ensembl.org/vep/{species}/region/{region}/{allele}/", headers={"Content-Type": "application/json"}, 
                               params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
    return response.json()


# def _vep_region_post(variants:list,species='human',AncestralAllele=None,Blosum62=None,CADD=None,Conservation=None,DisGeNET=None,EVE=None,GO=None,GeneSplicer=None,IntAct=None,LoF=None,Mastermind=None,MaxEntScan=None,
# NMD=None,Phenotypes=None,SpliceAI=None,UTRAnnotator=None,ambiguous_hgvs=None,appris=None,canonical=None,ccds=None,dbNSFP=None,dbscSNV=None,distance=None,domains=None,failed=None,hgvs=None,mane=None,merged=None,minimal=None,
# mirna=None,mutfunc=None,numbers=None,protein=None,refseq=None,shift_3prime=None,shift_genomic=None,transcript_id=None,transcript_version=None,tsl=None,uniprot=None,variant_class=None,vcf_string=None,xref_refseq=None,format='json'):
#     response =requests.post(f"https://rest.ensembl.org/vep/{species}/region/", headers={"Content-Type": "application/json"}, json={"variants":variants},
#                                params=dict(AncestralAllele=AncestralAllele,Blosum62=Blosum62,CADD=CADD,Conservation=Conservation,DisGeNET=DisGeNET,EVE=EVE,GO=GO,GeneSplicer=GeneSplicer,IntAct=IntAct,LoF=LoF,Mastermind=Mastermind,MaxEntScan=MaxEntScan,
# NMD=NMD,Phenotypes=Phenotypes,SpliceAI=SpliceAI,UTRAnnotator=UTRAnnotator,appris=appris,canonical=canonical,ccds=ccds,dbNSFP=dbNSFP,dbscSNV=dbscSNV,distance=distance,domains=domains,failed=failed,hgvs=hgvs,mane=mane,merged=merged,minimal=minimal,
# mirna=mirna,mutfunc=mutfunc,numbers=numbers,protein=protein,refseq=refseq,shift_3prime=shift_3prime,shift_genomic=shift_genomic,transcript_id=transcript_id,transcript_version=transcript_version,tsl=tsl,uniprot=uniprot,variant_class=variant_class,vcf_string=vcf_string,xref_refseq=xref_refseq,format=format))
#     return response.json()

def _vep_region_post(region:list,species='homo_sapiens',format='json'):
    response =requests.post(f"https://rest.ensembl.org/vep/{species}/region/", headers={"Content-Type": "application/json"}, json={"variants":region},
                               params=dict(format=format))
    return response.json()

def _ga4gh_beacon(format="json"):
        """Retrieves a cafe tree of the gene tree using the gene tree stable identifier"""
        response =requests.get(f"https://rest.ensembl.org/ga4gh/beacon", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
        return response.json()

def _ga4gh_beacon_query(alternateBases:str,assemblyId:str,referenceBases:str,referenceName:str,start:int,end=None,endMax=None,endMin=None,startMax=None,startMin=None,variantType=None,
                        datasetIds=None,includeDatasetResponses=None,format="json"):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/beacon/query", headers={"Content-Type": "application/json"}, 
                               params=dict(alternateBases=alternateBases,assemblyId=assemblyId,referenceBases=referenceBases,referenceName=referenceName,start=start,datasetIds=datasetIds,end=end,endMax=endMax,endMin=endMin,startMax=startMax,startMin=startMin,variantType=variantType,includeDatasetResponses=includeDatasetResponses))
    return response.json()

def _ga4gh_features(id:str,format="json"):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/features/{id}", headers={"Content-Type": "application/json"}, 
                               params=dict(format=format))
    return response.json()

def _ga4gh_features_search(end=None,referenceName=None,start=None,featureTypes=None,featureSetId=None,pageSize=None,pageToken=None,parentId=None,format="json"):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/features/search", headers={"Content-Type": "application/json"},json=dict(end=end,referenceName=referenceName,start=start,featureTypes=featureTypes,featureSetId=featureSetId,pageSize=pageSize,pageToken=pageToken,parentId=parentId,format=format),
                               params={})
    return response.json()

def _ga4gh_callsets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/callsets/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_datasets_search(pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/datasets/search", headers={"Content-Type": "application/json"}, json=dict(pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_callsets_search(variantSetId=None,name=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/callsets/search", headers={"Content-Type": "application/json"}, json=dict(variantSetId=variantSetId,name=name,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_datasets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/datasets/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_featuresets_search(datasetId=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/featuresets/search", headers={"Content-Type": "application/json"}, json=dict(datasetId=datasetId,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_featuresets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org//ga4gh/featuresets/Ensembl/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_variants(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/variants/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_variants_search(variantSetId=None,referenceName=None,start=None,end=None,callSetIds=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/variants/search", headers={"Content-Type": "application/json"}, json=dict(variantSetId=variantSetId,referenceName=referenceName,start=start,end=end,callSetIds=callSetIds,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_variantannotations_search(variantAnnotationSetId=None,effects=None,end=None,pageSize=None,pageToken=None,referenceId=None,referenceName=None,start=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/variantannotations/search", headers={"Content-Type": "application/json"}, json=dict(variantAnnotationSetId=variantAnnotationSetId,effects=effects,end=end,pageSize=pageSize,pageToken=pageToken,referenceId=referenceId,referenceName=referenceName,start=start),params=dict(format=format))
    return response.json()

def _ga4gh_variantsets_search(datasetId=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/variantsets/search", headers={"Content-Type": "application/json"}, json=dict(datasetId=datasetId,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_variantsets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/variantsets/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_references_search(referenceSetId=None,accession=None,md5checksum=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/references/search", headers={"Content-Type": "application/json"}, json=dict(referenceSetId=referenceSetId,accession=accession,md5checksum=md5checksum,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_references(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/references/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_referencesets_search(accession=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/referencesets/search", headers={"Content-Type": "application/json"}, json=dict(accession=accession,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_referencesets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/referencesets/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

def _ga4gh_variantannotationsets_search(variantSetId=None,pageSize=None,pageToken=None,format='json'):
    response =requests.post(f"https://rest.ensembl.org/ga4gh/variantannotationsets/search", headers={"Content-Type": "application/json"}, json=dict(variantSetId=variantSetId,pageSize=pageSize,pageToken=pageToken),params=dict(format=format))
    return response.json()

def _ga4gh_variantannotationsets(id:str,format='json'):
    response =requests.get(f"https://rest.ensembl.org/ga4gh/variantannotationsets/{id}", headers={"Content-Type": "application/json"}, params=dict(format=format))
    return response.json()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", help='variant sub-commands')
variant_recoder = subparsers.add_parser(
    'variant_recoder', help='variant_recoder help')
variant_recoder.add_argument('id', action='extend', nargs='+')
variant_recoder.add_argument('--format', default='json')
variant_recoder.add_argument('--species', default='human')
variant_recoder.add_argument('--fields', required=False, default=None)
variant_recoder.add_argument('--var_synonyms', default=None)
variant_recoder.add_argument("--vcf_string", default=None)

variation = subparsers.add_parser('variation', help='variant help')
variation.add_argument('id', action='extend', nargs='+')
variation.add_argument('--format', default='json')
variation.add_argument('--species', default='human')
variation.add_argument('--pops', default=None)
variation.add_argument('--genotypes', default=None)
variation.add_argument('--genotyping_chips', default=None)
variation.add_argument('--phenotypes', default=None)
variation.add_argument('--population_genotypes', default=None)

variation_pmcid=subparsers.add_parser('variation_pmcid', help='variation_pmcid')
variation_pmcid.add_argument('pmcid')
variation_pmcid.add_argument('--format', default='json')
variation_pmcid.add_argument('--species', default='human')

variation_pmid=subparsers.add_parser('variation_pmid', help='variation_pmid')
variation_pmid.add_argument('pmid')
variation_pmid.add_argument('--format', default='json')
variation_pmid.add_argument('--species', default='human')

archive = subparsers.add_parser('archive', help='archive help')
archive.add_argument('id', action='extend', nargs='+')
archive.add_argument('--format', default='json')

cafe_genetree_id = subparsers.add_parser(
    'cafe_genetree_id', help='cafe_genetree_id help')
cafe_genetree_id.add_argument('id')
cafe_genetree_id.add_argument('--format', default='json')
cafe_genetree_id.add_argument('--compara', default=None)
cafe_genetree_id.add_argument('--nh_format', default=None)


cafe_genetree_member = subparsers.add_parser(
    'cafe_genetree_member', help='cafe_genetree_member help')
cafe_genetree_member.add_argument('id')
cafe_genetree_member.add_argument('--format', default='json')
cafe_genetree_member.add_argument('--compara', default=None)
cafe_genetree_member.add_argument('--db_type', default=None)
cafe_genetree_member.add_argument('--nh_format', default=None)
cafe_genetree_member.add_argument('--object_type', default=None)
cafe_genetree_member.add_argument('--species', default=None)


cafe_genetree_member_symbol=subparsers.add_parser('cafe_genetree_member_symbol',help='cafe_genetree_member_symbol help')
cafe_genetree_member_symbol.add_argument('symbol')
cafe_genetree_member_symbol.add_argument('--format', default='json')
cafe_genetree_member_symbol.add_argument('--species', default='homo_sapiens')
cafe_genetree_member_symbol.add_argument('--compara', default=None)
cafe_genetree_member_symbol.add_argument('--db_type', default=None)
cafe_genetree_member_symbol.add_argument('--external_db', default=None)
cafe_genetree_member_symbol.add_argument('--nh_format', default=None)
cafe_genetree_member_symbol.add_argument('--object_type', default=None)

genetree_id=subparsers.add_parser('genetree_id',help='genetree_id help')
genetree_id.add_argument('id')
genetree_id.add_argument('--format', default='json')
genetree_id.add_argument('--aligned', default=None)
genetree_id.add_argument('--cigar_line', default=None)
genetree_id.add_argument('--clusterset_id', default=None)
genetree_id.add_argument('--compara', default=None)
genetree_id.add_argument('--nh_format', default=None)
genetree_id.add_argument('--prune_species', default=None)
genetree_id.add_argument('--prune_taxon', default=None)
genetree_id.add_argument('--sequence', default=None)

genetree_member_id=subparsers.add_parser('genetree_member_id',help='genetree_member_id help')
genetree_member_id.add_argument('id')
genetree_member_id.add_argument('--format', default='json')
genetree_member_id.add_argument('--aligned', default=None)
genetree_member_id.add_argument('--cigar_line', default=None)
genetree_member_id.add_argument('--clusterset_id', default=None)
genetree_member_id.add_argument('--compara', default=None)
genetree_member_id.add_argument('--db_type', default=None)
genetree_member_id.add_argument('--nh_format', default=None)
genetree_member_id.add_argument('--object_type', default=None)
genetree_member_id.add_argument('--prune_species', default=None)
genetree_member_id.add_argument('--prune_taxon', default=None)
genetree_member_id.add_argument('--sequence', default=None)
genetree_member_id.add_argument('--species', default=None)

genetree_member_symbol=subparsers.add_parser('genetree_member_symbol',help='genetree_member_symbol help')
genetree_member_symbol.add_argument('symbol')
genetree_member_symbol.add_argument('--format', default='json')
genetree_member_symbol.add_argument('--species', default='homo_sapiens')
genetree_member_symbol.add_argument('--aligned', default=None)
genetree_member_symbol.add_argument('--cigar_line', default=None)
genetree_member_symbol.add_argument('--clusterset_id', default=None)
genetree_member_symbol.add_argument('--compara', default=None)
genetree_member_symbol.add_argument('--db_type', default=None)
genetree_member_symbol.add_argument('--external_db', default=None)
genetree_member_symbol.add_argument('--nh_format', default=None)
genetree_member_symbol.add_argument('--object_type', default=None)
genetree_member_symbol.add_argument('--prune_species', default=None)
genetree_member_symbol.add_argument('--prune_taxon', default=None)
genetree_member_symbol.add_argument('--sequence', default=None)

alignment_region=subparsers.add_parser('alignment_region',help='alignment_region help')
alignment_region.add_argument('region')
alignment_region.add_argument('--format', default='json')
alignment_region.add_argument('--species', default='homo_sapiens')
alignment_region.add_argument('--aligned', default=None)
alignment_region.add_argument('--compact', default=None)
alignment_region.add_argument('--compara', default=None)
alignment_region.add_argument('--display_species_set', default=None)
alignment_region.add_argument('--mask', default=None)
alignment_region.add_argument('--method', default=None)
alignment_region.add_argument('--species_set', default=None)
alignment_region.add_argument('--species_set_group', default=None)

homology_id=subparsers.add_parser('homology_id',help='homology_id help')
homology_id.add_argument('id')
homology_id.add_argument('--format', default=None)
homology_id.add_argument('--aligned', default=None)
homology_id.add_argument('--cigar_line', default=None)
homology_id.add_argument('--compara', default=None)
homology_id.add_argument('--sequence', default=None)
homology_id.add_argument('--target_species', default=None)
homology_id.add_argument('--target_taxon', default=None)
homology_id.add_argument('--type', default=None)

homology_symbol=subparsers.add_parser('homology_symbol',help='homology_symbol help')
homology_symbol.add_argument('symbol')
homology_symbol.add_argument('--format', default=None)
homology_symbol.add_argument('--species', default='homo_sapiens')
homology_symbol.add_argument('--aligned', default=None)
homology_symbol.add_argument('--cigar_line', default=None)
homology_symbol.add_argument('--compara', default=None)
homology_symbol.add_argument('--external_db', default=None)
homology_symbol.add_argument('--sequence', default=None)
homology_symbol.add_argument('--target_species', default=None)
homology_symbol.add_argument('--target_taxon', default=None)
homology_symbol.add_argument('--type', default=None)

xrefs_symbol=subparsers.add_parser('xrefs_symbol',help='xrefs_symbol help')
xrefs_symbol.add_argument('symbol')
xrefs_symbol.add_argument('--format', default='json')
xrefs_symbol.add_argument('--species', default='homo_sapiens')
xrefs_symbol.add_argument('--db_type', default=None)
xrefs_symbol.add_argument('--external_db', default=None)
xrefs_symbol.add_argument('--object_type', default=None)

xrefs_id=subparsers.add_parser('xrefs_id',help='xrefs_id help')
xrefs_id.add_argument('id')
xrefs_id.add_argument('--format', default='json')
xrefs_id.add_argument('--all_levels', default=None)
xrefs_id.add_argument('--db_type', default=None)
xrefs_id.add_argument('--external_db', default=None)
xrefs_id.add_argument('--object_type', default=None)
xrefs_id.add_argument('--species', default=None)

xrefs_name=subparsers.add_parser('xrefs_name',help='xrefs_name help')
xrefs_name.add_argument('name')
xrefs_name.add_argument('--format', default='json')
xrefs_name.add_argument('--species', default='homo_sapiens')
xrefs_name.add_argument('--db_type', default=None)
xrefs_name.add_argument('--external_db', default=None)

info_analysis=subparsers.add_parser('info_analysis',help='info_analysis help')
info_analysis.add_argument('--format', default='json')
info_analysis.add_argument('--species',default='homo_sapiens')

info_assembly=subparsers.add_parser('info_assembly',help='info_assembly help')
info_assembly.add_argument('--format', default='json')
info_assembly.add_argument('--species', default='homo_sapiens')
info_assembly.add_argument('--bands',default=None)
info_assembly.add_argument('--synonyms',default=None)

info_assembly_region_name=subparsers.add_parser('info_assembly_region_name',help='info_assembly_region_name help')
info_assembly_region_name.add_argument('region_name')
info_assembly_region_name.add_argument('--format', default='json')
info_assembly_region_name.add_argument('--species', default='homo_sapiens')
info_assembly_region_name.add_argument('--bands',default=None)
info_assembly_region_name.add_argument('--synonyms',default=None)

info_biotypes=subparsers.add_parser('info_biotypes',help='info_biotypes help')
info_biotypes.add_argument('--format', default='json')
info_biotypes.add_argument('--species', default='homo_sapiens')

info_biotypes_group=subparsers.add_parser('info_biotypes_group',help='info_biotypes_group help')
info_biotypes_group.add_argument('--format', default='json')
info_biotypes_group.add_argument('--group',default=None)
info_biotypes_group.add_argument('--object_type',default=None)

info_biotypes_name=subparsers.add_parser('info_biotypes_name',help='info_biotypes_name help')
info_biotypes_name.add_argument('name')
info_biotypes_name.add_argument('--format', default='json')
info_biotypes_name.add_argument('--object_type',default=None)

info_compara_methods=subparsers.add_parser('info_compara_methods',help='info_compara_methods help')
info_compara_methods.add_argument('--format', default='json')
info_compara_methods.add_argument('--cla',default=None)
info_compara_methods.add_argument('--compara',default=None)

info_compara_species_sets=subparsers.add_parser('info_compara_species_sets',help='info_compara_species_sets help')
info_compara_species_sets.add_argument('method')
info_compara_species_sets.add_argument('--format', default='json')
info_compara_species_sets.add_argument('--compara',default=None)

info_comparas=subparsers.add_parser('info_comparas',help='info_comparas help')
info_comparas.add_argument('--format', default='json')

info_data=subparsers.add_parser('info_data',help='info_data help')
info_data.add_argument('--format', default='json')

info_eg_version=subparsers.add_parser('info_eg_version',help='info_eg_version help')
info_eg_version.add_argument('--format', default='json')

info_external_dbs=subparsers.add_parser('info_external_dbs',help='info_external_dbs help')
info_external_dbs.add_argument('--format', default='json')
info_external_dbs.add_argument('--species',default='homo_sapiens')
info_external_dbs.add_argument('--feature',default=None)
info_external_dbs.add_argument('--filter',default=None)

info_divisions=subparsers.add_parser('info_divisions',help='info_divisions help')
info_divisions.add_argument('--format', default='json')

info_genomes=subparsers.add_parser('info_genomes',help='info_genomes help')
info_genomes.add_argument('name')
info_genomes.add_argument('--format', default='json')
info_genomes.add_argument('--expand', default=None)

info_genomes_accession=subparsers.add_parser('info_genomes_accession',help='info_genomes_accession help')
info_genomes_accession.add_argument('accession')
info_genomes_accession.add_argument('--format', default='json')
info_genomes_accession.add_argument('--expand', default=None)

info_genomes_assembly=subparsers.add_parser('info_genomes_assembly',help='info_genomes_assembly help')
info_genomes_assembly.add_argument('assembly_id')
info_genomes_assembly.add_argument('--format', default='json')
info_genomes_assembly.add_argument('--expand', default=None)

info_genomes_division=subparsers.add_parser('info_genomes_division',help='info_genomes_division help')
info_genomes_division.add_argument('division')
info_genomes_division.add_argument('--format', default='json')
info_genomes_division.add_argument('--expand', default=None)

info_genomes_taxonomy=subparsers.add_parser('info_genomes_taxonomy',help='info_genomes_taxonomy help')
info_genomes_taxonomy.add_argument('taxon_name')
info_genomes_taxonomy.add_argument('--format', default='json')
info_genomes_taxonomy.add_argument('--expand', default=None)

info_ping=subparsers.add_parser('info_ping',help='info_ping help')
info_ping.add_argument('--format', default='json')

info_rest=subparsers.add_parser('info_rest',help='info_rest help')
info_rest.add_argument('--format', default='json')

info_software=subparsers.add_parser('info_software',help='info_software help')
info_software.add_argument('--format', default='json')

info_species=subparsers.add_parser('info_species',help='info_species help')
info_species.add_argument('--format', default='json')
info_species.add_argument('--division',default=None)
info_species.add_argument('--hide_strain_info',default=None)
info_species.add_argument('--strain_collection',default=None)

info_variation=subparsers.add_parser('info_variation',help='info_variation help')
info_variation.add_argument('--species',default='human')
info_variation.add_argument('--format', default='json')
info_variation.add_argument('--filter',default=None)

info_variation_consequence_types=subparsers.add_parser('info_variation_consequence_types',help='info_variation_consequence_types help')
info_variation_consequence_types.add_argument('--format', default='json')
info_variation_consequence_types.add_argument('--rank',default=None)

info_variation_populations=subparsers.add_parser('info_variation_populations',help='info_variation_populations help')
info_variation_populations.add_argument('population_name')
info_variation_populations.add_argument('--species',default='human')
info_variation_populations.add_argument('--format', default='json')

info_variation_species=subparsers.add_parser('info_variation_species',help='info_variation_species help')
info_variation_species.add_argument('--species',default='human')
info_variation_species.add_argument('--format', default='json')
info_variation_species.add_argument('--filter',default=None)

ld=subparsers.add_parser('ld',help='ld help')
ld.add_argument('id')
ld.add_argument('population_name')
ld.add_argument('--format', default='json')
ld.add_argument('--species',default='homo_sapiens')
ld.add_argument('--attribs',default=None)
ld.add_argument('--callback',default=None)
ld.add_argument('--d_prime',default=None)
ld.add_argument('--r2',default=None)
ld.add_argument('--window_size',default=None)

ld_pairwise=subparsers.add_parser('ld_pairwise',help='ld_pairwise help')
ld_pairwise.add_argument('id1')
ld_pairwise.add_argument('id2')
ld_pairwise.add_argument('--format', default='json')
ld_pairwise.add_argument('--species',default='human')
ld_pairwise.add_argument('--d_prime',default=None)
ld_pairwise.add_argument('--population_name',default=None)
ld_pairwise.add_argument('--r2',default=None)

ld_region=subparsers.add_parser('ld_region',help='ld_region help')
ld_region.add_argument('population_name')
ld_region.add_argument('region')
ld_region.add_argument('--format', default='json')
ld_region.add_argument('--species',default='human')
ld_region.add_argument('--d_prime',default=None)
ld_region.add_argument('--r2',default=None)

lookup_id = subparsers.add_parser('lookup_id', help='lookup_id help')
lookup_id.add_argument('id', action='extend', nargs='+')
lookup_id.add_argument('--format', default=None)
lookup_id.add_argument('--db_type', default=None)
lookup_id.add_argument('--expand', default=None)
lookup_id.add_argument('--mane', default=None)
lookup_id.add_argument('--phenotypes', default=None)
lookup_id.add_argument('--species', default=None)
lookup_id.add_argument('--utr', default=None)

lookup_symbol=subparsers.add_parser('lookup_symbol',help='lookup_symbol help')
lookup_symbol.add_argument('symbol')
lookup_symbol.add_argument('--format', default=None)
lookup_symbol.add_argument('--species',default='human')
lookup_symbol.add_argument('--expand',default=None)

map_cdna=subparsers.add_parser('map_cdna',help='map_cdna help')
map_cdna.add_argument('id')
map_cdna.add_argument('region')
map_cdna.add_argument('--format', default='json')
map_cdna.add_argument('--include_original_region',default=None)
map_cdna.add_argument('--species',default=None)

map_cds=subparsers.add_parser('map_cds',help='map_cds help')
map_cds.add_argument('id')
map_cds.add_argument('region')
map_cds.add_argument('--format', default='json')
map_cds.add_argument('--include_original_region',default=None)
map_cds.add_argument('--species',default=None)

map_assembly=subparsers.add_parser('map_assembly',help='map_assembly help')
map_assembly.add_argument('asm_one')
map_assembly.add_argument('asm_two')
map_assembly.add_argument('region')
map_assembly.add_argument('--format', default='json')
map_assembly.add_argument('--species',default='human')
map_assembly.add_argument('--coord_system',default=None)
map_assembly.add_argument('--target_coord_system',default=None)

map_translation=subparsers.add_parser('map_translation',help='map_translation help')
map_translation.add_argument('id')
map_translation.add_argument('region')
map_translation.add_argument('--format', default='json')
map_translation.add_argument('--species',default=None)

ontology_ancestors=subparsers.add_parser('ontology_ancestors',help='ontology_ancestors help')
ontology_ancestors.add_argument('id')
ontology_ancestors.add_argument('--format', default='json')
ontology_ancestors.add_argument('--ontology',default=None)

ontology_ancestors_chart=subparsers.add_parser('ontology_ancestors_chart',help='ontology_ancestors_chart help')
ontology_ancestors_chart.add_argument('id')
ontology_ancestors_chart.add_argument('--format', default='json')
ontology_ancestors_chart.add_argument('--ontology',default=None)

ontology_descendants=subparsers.add_parser('ontology_descendants',help='ontology_descendants help')
ontology_descendants.add_argument('id')
ontology_descendants.add_argument('--format', default='json')
ontology_descendants.add_argument('--closest_term',default=None)
ontology_descendants.add_argument('--ontology',default=None)
ontology_descendants.add_argument('--subset',default=None)
ontology_descendants.add_argument('--zero_distance',default=None)

ontology_id=subparsers.add_parser('ontology_id',help='ontology_id help')
ontology_id.add_argument('id')
ontology_id.add_argument('--format', default='json')
ontology_id.add_argument('--relation',default=None)
ontology_id.add_argument('--simple',default=None)

ontology_name=subparsers.add_parser('ontology_name',help='ontology_name help')
ontology_name.add_argument('name')
ontology_name.add_argument('--format', default='json')
ontology_name.add_argument('--ontology',default=None)
ontology_name.add_argument('--relation',default=None)
ontology_name.add_argument('--simple',default=None)

taxonomy_classification=subparsers.add_parser('taxonomy_classification',help='taxonomy_classification help')
taxonomy_classification.add_argument('id')
taxonomy_classification.add_argument('--format', default='json')

taxonomy_id=subparsers.add_parser('taxonomy_id',help='taxonomy_id help')
taxonomy_id.add_argument('id')
taxonomy_id.add_argument('--format', default='json')
taxonomy_id.add_argument('--simple',default=None)

taxonomy_name=subparsers.add_parser('taxonomy_name',help='taxonomy_name help')
taxonomy_name.add_argument('name')
taxonomy_name.add_argument('--format', default='json')

overlap_id=subparsers.add_parser('overlap_id',help='overlap_id help')
overlap_id.add_argument('id')
overlap_id.add_argument('--format', default='json')
overlap_id.add_argument('feature',default=None)
overlap_id.add_argument('--biotype',default=None)
overlap_id.add_argument('--db_type',default=None)
overlap_id.add_argument('--logic_name',default=None)
overlap_id.add_argument('--misc_set',default=None)
overlap_id.add_argument('--object_type',default=None)
overlap_id.add_argument('--so_term',default=None)
overlap_id.add_argument('--species',default=None)
overlap_id.add_argument('--species_set',default=None)
overlap_id.add_argument('--variant_set',default=None)

overlap_region=subparsers.add_parser('overlap_region',help='overlap_region help')
overlap_region.add_argument('region')
overlap_region.add_argument('feature',default=None)
overlap_region.add_argument('--format', default='json')
overlap_region.add_argument('--species',default='homo_sapiens')
overlap_region.add_argument('--biotype',default=None)
overlap_region.add_argument('--db_type',default=None)
overlap_region.add_argument('--logic_name',default=None)
overlap_region.add_argument('--misc_set',default=None)
overlap_region.add_argument('--so_term',default=None)
overlap_region.add_argument('--species_set',default=None)
overlap_region.add_argument('--trim_downstream',default=None)
overlap_region.add_argument('--trim_upstream',default=None)
overlap_region.add_argument('--variant_set',default=None)

overlap_translation=subparsers.add_parser('overlap_translation',help='overlap_translation help')
overlap_translation.add_argument('id')
overlap_translation.add_argument('--format', default='json')
overlap_translation.add_argument('--db_type',default=None)
overlap_translation.add_argument('--feature',default=None)
overlap_translation.add_argument('--so_term',default=None)
overlap_translation.add_argument('--species',default=None)
overlap_translation.add_argument('--type',default=None)

phenotype_accession=subparsers.add_parser('phenotype_accession',help='phenotype_accession help')
phenotype_accession.add_argument('accession')
phenotype_accession.add_argument('--species', default='homo_sapiens')
phenotype_accession.add_argument('--format', default='json')
phenotype_accession.add_argument('--include_children',default=None)
phenotype_accession.add_argument('--include_pubmed_id',default=None)
phenotype_accession.add_argument('--include_review_status',default=None)
phenotype_accession.add_argument('--source',default=None)

phenotype_gene=subparsers.add_parser('phenotype_gene',help='phenotype_gene help')
phenotype_gene.add_argument('gene')
phenotype_gene.add_argument('--species', default='homo_sapiens')
phenotype_gene.add_argument('--format', default='json')
phenotype_gene.add_argument('--include_associated',default=None)
phenotype_gene.add_argument('--include_overlap',default=None)
phenotype_gene.add_argument('--include_pubmed_id',default=None)
phenotype_gene.add_argument('--include_review_status',default=None)
phenotype_gene.add_argument('--include_submitter',default=None)
phenotype_gene.add_argument('--non_specified',default=None)
phenotype_gene.add_argument('--trait',default=None)
phenotype_gene.add_argument('--tumour',default=None)

phenotype_region=subparsers.add_parser('phenotype_region',help='phenotype_region help')
phenotype_region.add_argument('region')
phenotype_region.add_argument('--species',default='homo_sapiens')
phenotype_region.add_argument('--format', default='json')
phenotype_region.add_argument('--feature_type',default=None)
phenotype_region.add_argument('--include_pubmed_id',default=None)
phenotype_region.add_argument('--include_review_status',default=None)
phenotype_region.add_argument('--include_submitter',default=None)
phenotype_region.add_argument('--non_specified',default=None)
phenotype_region.add_argument('--only_phenotypes',default=None)
phenotype_region.add_argument('--trait',default=None)
phenotype_region.add_argument('--tumour',default=None)

phenotype_term=subparsers.add_parser('phenotype_term',help='phenotype_term help')
phenotype_term.add_argument('term')
phenotype_term.add_argument('--format', default='json')
phenotype_term.add_argument('--species',default='homo_sapiens')
phenotype_term.add_argument('--include_children',default=None)
phenotype_term.add_argument('--include_pubmed_id',default=None)
phenotype_term.add_argument('--include_review_status',default=None)
phenotype_term.add_argument('--source',default=None)

regulatory_microarray_vendor=subparsers.add_parser('regulatory_microarray_vendor',help='regulatory_microarray_vendor help')
regulatory_microarray_vendor.add_argument('microarray')
regulatory_microarray_vendor.add_argument('vendor')
regulatory_microarray_vendor.add_argument('--format', default='json')
regulatory_microarray_vendor.add_argument('--species',default='homo_sapiens')

regulatory_species=subparsers.add_parser('regulatory_species',help='regulatory_species help')
regulatory_species.add_argument('--format', default='json')
regulatory_species.add_argument('--species',default='homo_sapiens')

species_binding_matrix=subparsers.add_parser('species_binding_matrix',help='species_binding_matrix help')
species_binding_matrix.add_argument('binding_matrix')
species_binding_matrix.add_argument('--format', default='json')
species_binding_matrix.add_argument('--species',default='homo_sapiens')
species_binding_matrix.add_argument('--unit',default=None)

regulatory_microarray=subparsers.add_parser('regulatory_microarray',help='regulatory_microarray help')
regulatory_microarray.add_argument('--format', default='json')
regulatory_microarray.add_argument('--species',default='homo_sapiens')

regulatory_probe=subparsers.add_parser('regulatory_probe',help='regulatory_probe help')
regulatory_probe.add_argument('microarray')
regulatory_probe.add_argument('probe')
regulatory_probe.add_argument('--format', default='json')
regulatory_probe.add_argument('--species',default='homo_sapiens')
regulatory_probe.add_argument('--gene',default=None)
regulatory_probe.add_argument('--transcripts',default=None)

regulatory_probe_set=subparsers.add_parser('regulatory_probe_set',help='regulatory_probe_set help')
regulatory_probe_set.add_argument('microarray')
regulatory_probe_set.add_argument('probe_set')
regulatory_probe_set.add_argument('--format', default='json')
regulatory_probe_set.add_argument('--species',default='homo_sapiens')
regulatory_probe_set.add_argument('--gene',default=None)
regulatory_probe_set.add_argument('--transcripts',default=None)

regulatory_id=subparsers.add_parser('regulatory_id',help='regulatory_id help')
regulatory_id.add_argument('id')
regulatory_id.add_argument('--format', default='json')
regulatory_id.add_argument('--species',default='homo_sapiens')
regulatory_id.add_argument('--activity',default=None)

sequence_id= subparsers.add_parser('sequence_id', help='sequence_id help')
sequence_id.add_argument('id', action='extend', nargs='+')
sequence_id.add_argument('--format', default=None)
sequence_id.add_argument('--db_type',default=None)
sequence_id.add_argument('--end',default=None)
sequence_id.add_argument('--expand_3prime',default=None)
sequence_id.add_argument('--expand_5prime',default=None)
sequence_id.add_argument('--mask',default=None)
sequence_id.add_argument('--mask_feature',default=None)
sequence_id.add_argument('--multiple_sequences',default=None)
sequence_id.add_argument('--object_type',default=None)
sequence_id.add_argument('--species',default=None)
sequence_id.add_argument('--start',default=None)
sequence_id.add_argument('--type',default=None)

sequence_region= subparsers.add_parser('sequence_region', help='sequence_region help')
sequence_region.add_argument('region', action='extend', nargs='+')
sequence_region.add_argument('--format', default=None)
sequence_region.add_argument('--species',default='human')
sequence_region.add_argument('--coord_system',default=None)
sequence_region.add_argument('--coord_system_version',default=None)
sequence_region.add_argument('--expand_3prime',default=None)
sequence_region.add_argument('--expand_5prime',default=None)
sequence_region.add_argument('--mask',default=None)
sequence_region.add_argument('--mask_feature',default=None)

transcript_haplotypes=subparsers.add_parser('transcript_haplotypes', help='transcript_haplotypes help')
transcript_haplotypes.add_argument('id')
transcript_haplotypes.add_argument('--format', default='json')
transcript_haplotypes.add_argument('--species',default='homo_sapiens')
transcript_haplotypes.add_argument('--aligned_sequences',default=None)
transcript_haplotypes.add_argument('--samples',default=None)
transcript_haplotypes.add_argument('--sequence',default=None)

vep_hgvs=subparsers.add_parser('vep_hgvs',help='vep_hgvs help')
vep_hgvs.add_argument('hgvs_notation',action='extend', nargs='+')
vep_hgvs.add_argument('--species',default='homo_sapiens')
vep_hgvs.add_argument('--format', default='json')
vep_hgvs.add_argument('--AncestralAllele',default=None)
vep_hgvs.add_argument('--Blosum62',default=None)
vep_hgvs.add_argument('--CADD',default=None)
vep_hgvs.add_argument('--Conservation',default=None)
vep_hgvs.add_argument('--DisGeNET',default=None)
vep_hgvs.add_argument('--EVE',default=None)
vep_hgvs.add_argument('--GO',default=None)
vep_hgvs.add_argument('--GeneSplicer',default=None)
vep_hgvs.add_argument('--IntAct',default=None)
vep_hgvs.add_argument('--LoF',default=None)
vep_hgvs.add_argument('--Mastermind',default=None)
vep_hgvs.add_argument('--MaxEntScan',default=None)
vep_hgvs.add_argument('--NMD',default=None)
vep_hgvs.add_argument('--Phenotypes',default=None)
vep_hgvs.add_argument('--SpliceAI',default=None)
vep_hgvs.add_argument('--UTRAnnotator',default=None)
vep_hgvs.add_argument('--ambiguous_hgvs',default=None)
vep_hgvs.add_argument('--appris',default=None)
vep_hgvs.add_argument('--callback',default=None)
vep_hgvs.add_argument('--canonical',default=None)
vep_hgvs.add_argument('--ccds',default=None)
vep_hgvs.add_argument('--dbNSFP',default=None)
vep_hgvs.add_argument('--dbscSNV',default=None)
vep_hgvs.add_argument('--distance',default=None)
vep_hgvs.add_argument('--domains',default=None)
vep_hgvs.add_argument('--failed',default=None)
vep_hgvs.add_argument('--hgvs',default=None)
vep_hgvs.add_argument('--mane',default=None)
vep_hgvs.add_argument('--merged',default=None)
vep_hgvs.add_argument('--minimal',default=None)
vep_hgvs.add_argument('--mirna',default=None)
vep_hgvs.add_argument('--mutfunc',default=None)
vep_hgvs.add_argument('--numbers',default=None)
vep_hgvs.add_argument('--protein',default=None)
vep_hgvs.add_argument('--refseq',default=None)
vep_hgvs.add_argument('--shift_3prime',default=None)
vep_hgvs.add_argument('--shift_genomic',default=None)
vep_hgvs.add_argument('--transcript_id',default=None)
vep_hgvs.add_argument('--transcript_version',default=None)
vep_hgvs.add_argument('--tsl',default=None)
vep_hgvs.add_argument('--uniprot',default=None)
vep_hgvs.add_argument('--variant_class',default=None)
vep_hgvs.add_argument('--vcf_string',default=None)
vep_hgvs.add_argument('--xref_refseq',default=None)

vep_id=subparsers.add_parser('vep_id',help='vep_id help')
vep_id.add_argument('id', action='extend', nargs='+')
vep_id.add_argument('--species',default='homo_sapiens')
vep_id.add_argument('--format', default='json')
vep_id.add_argument('--AncestralAllele',default=None)
vep_id.add_argument('--Blosum62',default=None)
vep_id.add_argument('--CADD',default=None)
vep_id.add_argument('--Conservation',default=None)
vep_id.add_argument('--DisGeNET',default=None)
vep_id.add_argument('--EVE',default=None)
vep_id.add_argument('--GO',default=None)
vep_id.add_argument('--GeneSplicer',default=None)
vep_id.add_argument('--IntAct',default=None)
vep_id.add_argument('--LoF',default=None)
vep_id.add_argument('--Mastermind',default=None)
vep_id.add_argument('--MaxEntScan',default=None)
vep_id.add_argument('--NMD',default=None)
vep_id.add_argument('--Phenotypes',default=None)
vep_id.add_argument('--SpliceAI',default=None)
vep_id.add_argument('--UTRAnnotator',default=None)
vep_id.add_argument('--appris',default=None)
vep_id.add_argument('--callback',default=None)
vep_id.add_argument('--canonical',default=None)
vep_id.add_argument('--ccds',default=None)
vep_id.add_argument('--dbNSFP',default=None)
vep_id.add_argument('--dbscSNV',default=None)
vep_id.add_argument('--distance',default=None)
vep_id.add_argument('--domains',default=None)
vep_id.add_argument('--failed',default=None)
vep_id.add_argument('--hgvs',default=None)
vep_id.add_argument('--mane',default=None)
vep_id.add_argument('--merged',default=None)
vep_id.add_argument('--minimal',default=None)
vep_id.add_argument('--mirna',default=None)
vep_id.add_argument('--mutfunc',default=None)
vep_id.add_argument('--numbers',default=None)
vep_id.add_argument('--protein',default=None)
vep_id.add_argument('--refseq',default=None)
vep_id.add_argument('--shift_3prime',default=None)
vep_id.add_argument('--shift_genomic',default=None)
vep_id.add_argument('--transcript_id',default=None)
vep_id.add_argument('--transcript_version',default=None)
vep_id.add_argument('--tsl',default=None)
vep_id.add_argument('--uniprot',default=None)
vep_id.add_argument('--variant_class',default=None)
vep_id.add_argument('--vcf_string',default=None)
vep_id.add_argument('--xref_refseq',default=None)

vep_region_get=subparsers.add_parser('vep_region_get',help='vep_region_get help')
vep_region_get.add_argument('allele')
vep_region_get.add_argument('region')
vep_region_get.add_argument('--species',default='homo_sapiens')
vep_region_get.add_argument('--format', default='json')
vep_region_get.add_argument('--AncestralAllele',default=None)
vep_region_get.add_argument('--Blosum62',default=None)
vep_region_get.add_argument('--CADD',default=None)
vep_region_get.add_argument('--Conservation',default=None)
vep_region_get.add_argument('--DisGeNET',default=None)
vep_region_get.add_argument('--EVE',default=None)
vep_region_get.add_argument('--GO',default=None)
vep_region_get.add_argument('--GeneSplicer',default=None)
vep_region_get.add_argument('--IntAct',default=None)
vep_region_get.add_argument('--LoF',default=None)
vep_region_get.add_argument('--Mastermind',default=None)
vep_region_get.add_argument('--MaxEntScan',default=None)
vep_region_get.add_argument('--NMD',default=None)
vep_region_get.add_argument('--Phenotypes',default=None)
vep_region_get.add_argument('--SpliceAI',default=None)
vep_region_get.add_argument('--UTRAnnotator',default=None)
vep_region_get.add_argument('--appris',default=None)
vep_region_get.add_argument('--callback',default=None)
vep_region_get.add_argument('--canonical',default=None)
vep_region_get.add_argument('--ccds',default=None)
vep_region_get.add_argument('--dbNSFP',default=None)
vep_region_get.add_argument('--dbscSNV',default=None)
vep_region_get.add_argument('--distance',default=None)
vep_region_get.add_argument('--domains',default=None)
vep_region_get.add_argument('--failed',default=None)
vep_region_get.add_argument('--hgvs',default=None)
vep_region_get.add_argument('--mane',default=None)
vep_region_get.add_argument('--merged',default=None)
vep_region_get.add_argument('--minimal',default=None)
vep_region_get.add_argument('--mirna',default=None)
vep_region_get.add_argument('--mutfunc',default=None)
vep_region_get.add_argument('--numbers',default=None)
vep_region_get.add_argument('--protein',default=None)
vep_region_get.add_argument('--refseq',default=None)
vep_region_get.add_argument('--shift_3prime',default=None)
vep_region_get.add_argument('--shift_genomic',default=None)
vep_region_get.add_argument('--transcript_id',default=None)
vep_region_get.add_argument('--transcript_version',default=None)
vep_region_get.add_argument('--tsl',default=None)
vep_region_get.add_argument('--uniprot',default=None)
vep_region_get.add_argument('--variant_class',default=None)
vep_region_get.add_argument('--vcf_string',default=None)
vep_region_get.add_argument('--xref_refseq',default=None)

vep_region_post=subparsers.add_parser('vep_region_post',help='vep_region_post help')
vep_region_post.add_argument('region')
vep_region_post.add_argument('--species',default='homo_sapiens')
vep_region_post.add_argument('--format', default='json')
# vep_region_post.add_argument('--AncestralAllele',default=None)
# vep_region_post.add_argument('--Blosum62',default=None)
# vep_region_post.add_argument('--CADD',default=None)
# vep_region_post.add_argument('--Conservation',default=None)
# vep_region_post.add_argument('--DisGeNET',default=None)
# vep_region_post.add_argument('--EVE',default=None)
# vep_region_post.add_argument('--GO',default=None)
# vep_region_post.add_argument('--GeneSplicer',default=None)
# vep_region_post.add_argument('--IntAct',default=None)
# vep_region_post.add_argument('--LoF',default=None)
# vep_region_post.add_argument('--Mastermind',default=None)
# vep_region_post.add_argument('--MaxEntScan',default=None)
# vep_region_post.add_argument('--NMD',default=None)
# vep_region_post.add_argument('--Phenotypes',default=None)
# vep_region_post.add_argument('--SpliceAI',default=None)
# vep_region_post.add_argument('--UTRAnnotator',default=None)
# vep_region_post.add_argument('--appris',default=None)
# vep_region_post.add_argument('--callback',default=None)
# vep_region_post.add_argument('--canonical',default=None)
# vep_region_post.add_argument('--ccds',default=None)
# vep_region_post.add_argument('--dbNSFP',default=None)
# vep_region_post.add_argument('--dbscSNV',default=None)
# vep_region_post.add_argument('--distance',default=None)
# vep_region_post.add_argument('--domains',default=None)
# vep_region_post.add_argument('--failed',default=None)
# vep_region_post.add_argument('--hgvs',default=None)
# vep_region_post.add_argument('--mane',default=None)
# vep_region_post.add_argument('--merged',default=None)
# vep_region_post.add_argument('--minimal',default=None)
# vep_region_post.add_argument('--mirna',default=None)
# vep_region_post.add_argument('--mutfunc',default=None)
# vep_region_post.add_argument('--numbers',default=None)
# vep_region_post.add_argument('--protein',default=None)
# vep_region_post.add_argument('--refseq',default=None)
# vep_region_post.add_argument('--shift_3prime',default=None)
# vep_region_post.add_argument('--shift_genomic',default=None)
# vep_region_post.add_argument('--transcript_id',default=None)
# vep_region_post.add_argument('--transcript_version',default=None)
# vep_region_post.add_argument('--tsl',default=None)
# vep_region_post.add_argument('--uniprot',default=None)
# vep_region_post.add_argument('--variant_class',default=None)
# vep_region_post.add_argument('--vcf_string',default=None)
# vep_region_post.add_argument('--xref_refseq',default=None)

ga4gh_features=subparsers.add_parser('ga4gh_features',help='ga4gh_features help')
ga4gh_features.add_argument('id')
ga4gh_features.add_argument('--format', default='json')

ga4gh_beacon_query=subparsers.add_parser('ga4gh_beacon_query',help='ga4gh_beacon_query help')
ga4gh_beacon_query.add_argument('alternateBases')
ga4gh_beacon_query.add_argument('assemblyId')
ga4gh_beacon_query.add_argument('end')
ga4gh_beacon_query.add_argument('--endMax',default=None)
ga4gh_beacon_query.add_argument('--endMin',default=None)
ga4gh_beacon_query.add_argument('referenceBases')
ga4gh_beacon_query.add_argument('referenceName')
ga4gh_beacon_query.add_argument('start')
ga4gh_beacon_query.add_argument('--startMax',default=None)
ga4gh_beacon_query.add_argument('--startMin',default=None)
ga4gh_beacon_query.add_argument('--variantType',default=None)
ga4gh_beacon_query.add_argument('--format', default='json')
ga4gh_beacon_query.add_argument('--datasetIds', default=None)
ga4gh_beacon_query.add_argument('--includeDatasetResponses', default=None)

ga4gh_beacon=subparsers.add_parser('ga4gh_beacon',help='ga4gh_beacon help')
ga4gh_beacon.add_argument('--format', default='json')


ga4gh_callsets=subparsers.add_parser('ga4gh_callsets',help='ga4gh_callsets help')
ga4gh_callsets.add_argument('id')
ga4gh_callsets.add_argument('--format', default='json')

ga4gh_datasets_search=subparsers.add_parser('ga4gh_datasets_search',help='ga4gh_datasets_search help')
ga4gh_datasets_search.add_argument('--format', default='json')
ga4gh_datasets_search.add_argument('--pageSize',default=None)
ga4gh_datasets_search.add_argument('--pageToken',default=None)

ga4gh_callsets_search=subparsers.add_parser('ga4gh_callsets_search',help='ga4gh_callsets_search help')
ga4gh_callsets_search.add_argument('--format', default='json')
ga4gh_callsets_search.add_argument('--variantSetId',default=None)
ga4gh_callsets_search.add_argument('--pageSize',default=None)
ga4gh_callsets_search.add_argument('--pageToken',default=None)
ga4gh_callsets_search.add_argument('--name',default=None)

ga4gh_datasets=subparsers.add_parser('ga4gh_datasets',help='ga4gh_datasets help')
ga4gh_datasets.add_argument('id')
ga4gh_datasets.add_argument('--format', default='json')

ga4gh_featuresets_search=subparsers.add_parser('ga4gh_featuresets_search',help='ga4gh_featuresets_search help')
ga4gh_featuresets_search.add_argument('--format', default='json')
ga4gh_featuresets_search.add_argument('--datasetId',default=None)
ga4gh_featuresets_search.add_argument('--pageSize',default=None)
ga4gh_featuresets_search.add_argument('--pageToken',default=None)

ga4gh_featuresets=subparsers.add_parser('ga4gh_featuresets',help='ga4gh_featuresets help')
ga4gh_featuresets.add_argument('id')
ga4gh_featuresets.add_argument('--format', default='json')

ga4gh_variants=subparsers.add_parser('ga4gh_variants',help='ga4gh_variants help')
ga4gh_variants.add_argument('id')
ga4gh_variants.add_argument('--format', default='json')

ga4gh_variants_search=subparsers.add_parser('ga4gh_variants_search',help='ga4gh_variants_search help')
ga4gh_variants_search.add_argument('--format', default='json')
ga4gh_variants_search.add_argument('--variantSetId',default=None)
ga4gh_variants_search.add_argument('--referenceName',default=None)
ga4gh_variants_search.add_argument('--start',default=None)
ga4gh_variants_search.add_argument('--end',default=None)
ga4gh_variants_search.add_argument('--pageSize',default=None)
ga4gh_variants_search.add_argument('--pageToken',default=None)
ga4gh_variants_search.add_argument('--callSetIds',default=None)

ga4gh_variantannotations_search=subparsers.add_parser('ga4gh_variantannotations_search',help='ga4gh_variantannotations_search help')
ga4gh_variantannotations_search.add_argument('--format', default='json')
ga4gh_variantannotations_search.add_argument('--variantAnnotationSetId',default=None)
ga4gh_variantannotations_search.add_argument('--effects',default=None)
ga4gh_variantannotations_search.add_argument('--end',default=None)
ga4gh_variantannotations_search.add_argument('--pageSize',default=None)
ga4gh_variantannotations_search.add_argument('--pageToken',default=None)
ga4gh_variantannotations_search.add_argument('--referenceId',default=None)
ga4gh_variantannotations_search.add_argument('--referenceName',default=None)
ga4gh_variantannotations_search.add_argument('--start',default=None)

ga4gh_variantsets_search=subparsers.add_parser('ga4gh_variantsets_search',help='ga4gh_variantsets_search help')
ga4gh_variantsets_search.add_argument('--format', default='json')
ga4gh_variantsets_search.add_argument('--datasetId',default=None)
ga4gh_variantsets_search.add_argument('--pageSize',default=None)
ga4gh_variantsets_search.add_argument('--pageToken',default=None)

ga4gh_variantsets=subparsers.add_parser('ga4gh_variantsets',help='ga4gh_variantsets help')
ga4gh_variantsets.add_argument('id')
ga4gh_variantsets.add_argument('--format', default='json')

ga4gh_references_search=subparsers.add_parser('ga4gh_references_search',help='ga4gh_references_search help')
ga4gh_references_search.add_argument('--format', default='json')
ga4gh_references_search.add_argument('--pageSize',default=None)
ga4gh_references_search.add_argument('--pageToken',default=None)
ga4gh_references_search.add_argument('--accession',default=None)
ga4gh_references_search.add_argument('--md5checksum',default=None)
ga4gh_references_search.add_argument('--referenceSetId',default=None)

ga4gh_references=subparsers.add_parser('ga4gh_references',help='ga4gh_references help')
ga4gh_references.add_argument('id')
ga4gh_references.add_argument('--format', default='json')

ga4gh_referencesets_search=subparsers.add_parser('ga4gh_referencesets_search',help='ga4gh_referencesets_search help')
ga4gh_referencesets_search.add_argument('--format', default='json')
ga4gh_referencesets_search.add_argument('--pageSize',default=None)
ga4gh_referencesets_search.add_argument('--pageToken',default=None)
ga4gh_referencesets_search.add_argument('--accession',default=None)

ga4gh_referencesets=subparsers.add_parser('ga4gh_referencesets',help='ga4gh_referencesets help')
ga4gh_referencesets.add_argument('id')
ga4gh_referencesets.add_argument('--format', default='json')

ga4gh_variantannotationsets_search=subparsers.add_parser('ga4gh_variantannotationsets_search',help='ga4gh_variantannotationsets_search help')
ga4gh_variantannotationsets_search.add_argument('--format', default='json')
ga4gh_variantannotationsets_search.add_argument('--pageSize',default=None)
ga4gh_variantannotationsets_search.add_argument('--pageToken',default=None)
ga4gh_variantannotationsets_search.add_argument('--variantSetId',default=None)

ga4gh_variantannotationsets=subparsers.add_parser('ga4gh_variantannotationsets',help='ga4gh_variantannotationsets help')
ga4gh_variantannotationsets.add_argument('id')
ga4gh_variantannotationsets.add_argument('--format', default='json')

ga4gh_features_search=subparsers.add_parser('ga4gh_features_search',help='ga4gh_features_search help')
ga4gh_features_search.add_argument('--end', default=None)
ga4gh_features_search.add_argument('--referenceName', default=None)
ga4gh_features_search.add_argument('--start', default=None)
ga4gh_features_search.add_argument('--format', default='json')
ga4gh_features_search.add_argument('--featureTypes', default=None)
ga4gh_features_search.add_argument('--featureSetId', default=None)
ga4gh_features_search.add_argument('--pageSize', default=None)
ga4gh_features_search.add_argument('--pageToken', default=None)
ga4gh_features_search.add_argument('--parentId', default=None)

args = parser.parse_args()

if args.command == "variant_recoder":
    pprint.pprint(_variant_recoder(args.id, species=args.species, fields=args.fields,
                                   var_synonyms=args.var_synonyms, vcf_string=args.vcf_string, format=args.format))
elif args.command == "variation":
    pprint.pprint(_variation(args.id, species=args.species, pops=args.pops, genotypes=args.genotypes,
                  genotyping_chips=args.genotyping_chips, phenotypes=args.phenotypes, population_genotypes=args.population_genotypes))
elif args.command == "variation_pmcid":
    pprint.pprint(_variation_pmcid(args.pmcid,format=args.format))
elif args.command == "variation_pmid":
    pprint.pprint(_variation_pmid(args.pmid,format=args.format))
elif args.command == "archive":
    pprint.pprint(_archive(args.id))
elif args.command == "cafe_genetree_id":
    pprint.pprint(_cafe_genetree_id(args.id,compara=args.compara,nh_format=args.nh_format,format=args.format))
elif args.command == "cafe_genetree_member":
    pprint.pprint(_cafe_genetree_member(args.id,compara=args.compara,db_type=args.db_type,nh_format=args.nh_format,
                                        object_type=args.object_type,species=args.species,format=args.format))
elif args.command == "cafe_genetree_member_symbol":
    pprint.pprint(_cafe_genetree_member_symbol(args.symbol,compara=args.compara,db_type=args.db_type,external_db=args.external_db,nh_format=args.nh_format,
                                       object_type=args.object_type,format=args.format))
elif args.command == "genetree_id":
    pprint.pprint(_genetree_id(args.id,aligned=args.aligned,cigar_line=args.cigar_line,clusterset_id=args.clusterset_id,compara=args.compara,nh_format=args.nh_format,prune_species=args.prune_species,
                               prune_taxon=args.prune_taxon,sequence=args.sequence,format=args.format))
elif args.command == "genetree_member_id":
    pprint.pprint(_genetree_member_id(args.id,aligned=args.aligned,cigar_line=args.cigar_line,clusterset_id=args.clusterset_id,compara=args.compara,db_type=args.db_type,nh_format=args.nh_format,
                                        object_type=args.object_type,prune_species=args.prune_species,prune_taxon=args.prune_taxon,sequence=args.sequence,species=args.species,format=args.format))
elif args.command == "genetree_member_symbol":
    pprint.pprint(_genetree_member_symbol(args.symbol,aligned=args.aligned,cigar_line=args.cigar_line,clusterset_id=args.clusterset_id,compara=args.compara,db_type=args.db_type,external_db=args.external_db,nh_format=args.nh_format,
                                        object_type=args.object_type,prune_species=args.prune_species,prune_taxon=args.prune_taxon,sequence=args.sequence,format=args.format))
elif args.command == "alignment_region":
    pprint.pprint(_alignment_region(args.region,aligned=args.aligned,compact=args.compact,compara=args.compara,display_species_set=args.display_species_set,mask=args.mask,method=args.method,species_set=args.species_set,
                                           species_set_group=args.species_set_group,format=args.format))
elif args.command == "homology_id":
    pprint.pprint(_homology_id(args.id,aligned=args.aligned,cigar_line=args.cigar_line,compara=args.compara,sequence=args.sequence,target_species=args.target_species,target_taxon=args.target_taxon,
                                        type=args.type,format=args.format))
elif args.command == "homology_symbol":
    pprint.pprint(_homology_symbol(args.symbol,aligned=args.aligned,cigar_line=args.cigar_line,compara=args.compara,external_db=args.external_db,
                                           format=args.format,sequence=args.sequence,target_species=args.target_species,target_taxon=args.target_taxon,type=args.type))
elif args.command == "xrefs_symbol":
    pprint.pprint(_xrefs_symbol(args.symbol,db_type=args.db_type,external_db=args.external_db,object_type=args.object_type,format=args.format))
elif args.command == "xrefs_id":
    pprint.pprint(_xrefs_id(args.id,all_levels=args.all_levels,db_type=args.db_type,external_db=args.external_db,object_type=args.object_type,species=args.species,format=args.format))
elif args.command == "xrefs_name":
    pprint.pprint(_xrefs_name(args.name,db_type=args.db_type,external_db=args.external_db,format=args.format))
elif args.command == "info_analysis":
    pprint.pprint(_info_analysis(species=args.species,format=args.format))
elif args.command == "info_assembly":
    pprint.pprint(_info_assembly(species=args.species,format=args.format,bands=args.bands,synonyms=args.synonyms))
elif args.command == "info_assembly_region_name":
    pprint.pprint(_info_assembly_region_name(args.region_name,species=args.species,format=args.format,bands=args.bands,synonyms=args.synonyms))
elif args.command == "info_biotypes":
    pprint.pprint(_info_biotypes(species=args.species,format=args.format))
elif args.command == "info_biotypes_group":
    pprint.pprint(_info_biotypes_group(group=args.group,object_type=args.object_type,format=args.format))
elif args.command == "info_biotypes_name":
    pprint.pprint(_info_biotypes_name(name=args.name,object_type=args.object_type,format=args.format))
elif args.command == "info_compara_methods":
    pprint.pprint(_info_compara_methods(cla=args.cla,compara=args.compara,format=args.format))
elif args.command == "info_compara_species_sets":
    pprint.pprint(_info_compara_species_sets(args.method,compara=args.compara,format=args.format))
elif args.command == "info_comparas":
    pprint.pprint(_info_comparas(format=args.format))
elif args.command == "info_data":
    pprint.pprint(_info_data(format=args.format))
elif args.command == "info_eg_version":
    pprint.pprint(_info_eg_version(format=args.format))
elif args.command == "info_external_dbs":
    pprint.pprint(_info_external_dbs(feature=args.feature,filter=args.filter,format=args.format))
elif args.command =="info_divisions":
    pprint.pprint(_info_divisions(format=args.format))
elif args.command == "info_genomes":
    pprint.pprint(_info_genomes(args.name,expand=args.expand,format=args.format))
elif args.command == "info_genomes_accession":
    pprint.pprint(_info_genomes_accession(args.accession,expand=args.expand,format=args.format))
elif args.command == "info_genomes_assembly":
    pprint.pprint(_info_genomes_assembly(args.assembly_id,expand=args.expand,format=args.format))
elif args.command == "info_genomes_division":
    pprint.pprint(_info_genomes_division(args.division,expand=args.expand,format=args.format))
elif args.command == "info_ping":
    pprint.pprint(_info_ping(format=args.format))
elif args.command == "info_rest":
    pprint.pprint(_info_rest(format=args.format))
elif args.command == "info_software":
    pprint.pprint(_info_software(format=args.format))
elif args.command == "info_species":
    pprint.pprint(_info_species(division=args.division,hide_strain_info=args.hide_strain_info,strain_collection=args.strain_collection,format=args.format))
elif args.command == "info_variation":
    pprint.pprint(_info_variation(species=args.species,filter=args.filter,format=args.format))
elif args.command =="info_variation_consequence_types":
    pprint.pprint(_info_variation_consequence_types(rank=args.rank,format=args.format))
elif args.command == "info_variation_populations":
    pprint.pprint(_info_variation_populations(args.population_name,species=args.species,format=args.format))
elif args.command == "info_variation_species":
    pprint.pprint(_info_variation_species(species=args.species,filter=args.filter,format=args.format))
elif args.command == "ld":
    pprint.pprint(_ld(args.id,args.population_name,species=args.species,attribs=args.attribs,callback=args.callback,d_prime=args.d_prime,r2=args.r2,window_size=args.window_size,format=args.format))
elif args.command == "ld_pairwise":
    pprint.pprint(_ld_pairwise(args.id1,args.id2,species=args.species,d_prime=args.d_prime,population_name=args.population_name,r2=args.r2,format=args.format))
elif args.command == "ld_region":
    pprint.pprint(_ld_region(args.population_name,args.region,species=args.species,d_prime=args.d_prime,r2=args.r2,format=args.format))
elif args.command == "lookup_id":
    pprint.pprint(_lookup_id(args.id,db_type=args.db_type,expand=args.expand,mane=args.mane,phenotypes=args.phenotypes,
                               species=args.species,utr=args.utr,format=args.format))
elif args.command == "lookup_symbol":
    pprint.pprint(_lookup_symbol(args.symbol,species=args.species,expand=args.expand,format=args.format))
elif args.command == "map_cdna":
    pprint.pprint(_map_cdna(args.id,args.region,include_original_region=args.include_original_region,species=args.species,format=args.format))
elif args.command == "map_cds":
    pprint.pprint(_map_cds(args.id,args.region,include_original_region=args.include_original_region,species=args.species,format=args.format))
elif args.command == "map_assembly":
    pprint.pprint(_map_assembly(args.asm_one,args.asm_two,args.region,species=args.species,coord_system=args.coord_system,target_coord_system=args.target_coord_system,format=args.format))
elif args.command == "map_translation":
    pprint.pprint(_map_translation(args.id,args.region,species=args.species,format=args.format))
elif args.command == "ontology_ancestors":
    pprint.pprint(_ontology_ancestors(args.id,ontology=args.ontology,format=args.format))
elif args.command == "ontology_ancestors_chart":
    pprint.pprint(_ontology_ancestors_chart(args.id,ontology=args.ontology,format=args.format))
elif args.command == "ontology_descendants":
    pprint.pprint(_ontology_descendants(args.id,closest_term=args.closest_term,ontology=args.ontology,subset=args.subset,zero_distance=args.zero_distance,format=args.format))
elif args.command == "ontology_id":
    pprint.pprint(_ontology_id(args.id,relation=args.relation,simple=args.simple,format=args.format))
elif args.command == "ontology_name":
    pprint.pprint(_ontology_name(args.name,ontology=args.ontology,relation=args.relation,simple=args.simple,format=args.format))
elif args.command == "taxonomy_classification":
    pprint.pprint(_taxonomy_classification(args.id,format=args.format))
elif args.command == "taxonomy_id":
    pprint.pprint(_taxonomy_id(args.id,simple=args.simple,format=args.format))
elif args.command == "taxonomy_name":
    pprint.pprint(_taxonomy_name(args.name,format=args.format))
elif args.command == "overlap_id":
    pprint.pprint(_overlap_id(args.id,args.feature,biotype=args.biotype,db_type=args.db_type,logic_name=args.logic_name,misc_set=args.misc_set,object_type=args.object_type,so_term=args.so_term,species=args.species,
                                           species_set=args.species_set,variant_set=args.variant_set,format=args.format))
elif args.command == "overlap_region":
    pprint.pprint(_overlap_region(args.region,args.feature,species=args.species,biotype=args.biotype,db_type=args.db_type,logic_name=args.logic_name,misc_set=args.misc_set,so_term=args.so_term,
    species_set=args.species_set,trim_downstream=args.trim_downstream,trim_upstream=args.trim_upstream,variant_set=args.variant_set,format=args.format))
elif args.command == "overlap_translation":
    pprint.pprint(_overlap_translation(args.id,db_type=args.db_type,feature=args.feature,so_term=args.so_term,species=args.species,type=args.type,format=args.format))
elif args.command == "phenotype_accession":
    pprint.pprint(_phenotype_accession(args.accession,include_children=args.include_children,include_pubmed_id=args.include_pubmed_id,include_review_status=args.include_review_status,source=args.source,format=args.format))
elif args.command == "phenotype_gene":
    pprint.pprint(_phenotype_gene(args.gene,species=args.species,include_associated=args.include_associated,include_overlap=args.include_overlap,include_pubmed_id=args.include_pubmed_id,include_review_status=args.include_review_status,include_submitter=args.include_submitter,non_specified=args.non_specified,
                                           trait=args.trait,tumour=args.tumour,format=args.format))
elif args.command == "phenotype_region":
    pprint.pprint(_phenotype_region(args.region,species=args.species,feature_type=args.feature_type,include_pubmed_id=args.include_pubmed_id,include_review_status=args.include_review_status,include_submitter=args.include_submitter,non_specified=args.non_specified,only_phenotypes=args.only_phenotypes,trait=args.trait,tumour=args.tumour,format=args.format))
elif args.command == "phenotype_term":
    pprint.pprint(_phenotype_term(args.term,species=args.species,include_children=args.include_children,include_pubmed_id=args.include_pubmed_id,include_review_status=args.include_review_status,source=args.source,format=args.format))
elif args.command == "regulatory_microarray_vendor":
    pprint.pprint(_regulatory_microarray_vendor(args.microarray,args.vendor,species=args.species,format=args.format))
elif args.command == "regulatory_species":
    pprint.pprint(_regulatory_species(species=args.species,format=args.format))
elif args.command == "species_binding_matrix":
    pprint.pprint(_species_binding_matrix(args.binding_matrix,species=args.species,unit=args.unit,format=args.format))
elif args.command == "regulatory_microarray":
    pprint.pprint(_regulatory_microarray(args.species,format=args.format))
elif args.command == "regulatory_probe":
    pprint.pprint(_regulatory_probe(args.microarray,args.probe,species=args.species,gene=args.gene,transcripts=args.transcripts,format=args.format))
elif args.command == "regulatory_probe_set":
    pprint.pprint(_regulatory_probe_set(args.microarray,args.probe_set,species=args.species,gene=args.gene,transcripts=args.transcripts,format=args.format))
elif args.command == "regulatory_id":
    pprint.pprint(_regulatory_id(args.id,species=args.species,activity=args.activity,format=args.format))
elif args.command == "sequence_id":
    pprint.pprint(_sequence_id(args.id,db_type=args.db_type,end=args.end,expand_3prime=args.expand_3prime,expand_5prime=args.expand_5prime,mask=args.mask,mask_feature=args.mask_feature,multiple_sequences=args.multiple_sequences,object_type=args.object_type,species=args.species,start=args.start,type=args.type,format=args.format))
elif args.command == "sequence_region":
    pprint.pprint(_sequence_region(args.region,species=args.species,coord_system=args.coord_system,coord_system_version=args.coord_system_version,expand_3prime=args.expand_3prime,expand_5prime=args.expand_5prime,mask=args.mask,mask_feature=args.mask_feature,format=args.format))
elif args.command == "transcript_haplotypes":
    pprint.pprint(_transcript_haplotypes(args.id,species=args.species,aligned_sequences=args.aligned_sequences,samples=args.samples,sequence=args.sequence,format=args.format))
elif args.command == "_vep_hgvs":
    pprint.pprint(_vep_hgvs(args.hgvs,species=args.species,format=args.format))
elif args.command == "vep_hgvs":
    pprint.pprint(_vep_hgvs(args.hgvs_notation,species=args.species,format=args.format,AncestralAllele=args.AncestralAllele,Blosum62=args.Blosum62,CADD=args.CADD,Conservation=args.Conservation,DisGeNET=args.DisGeNET,EVE=args.EVE,GO=args.GO,GeneSplicer=args.GeneSplicer,IntAct=args.IntAct,LoF=args.LoF,Mastermind=args.Mastermind,MaxEntScan=args.MaxEntScan,
NMD=args.NMD,Phenotypes=args.Phenotypes,SpliceAI=args.SpliceAI,UTRAnnotator=args.UTRAnnotator,ambiguous_hgvs=args.ambiguous_hgvs,appris=args.appris,canonical=args.canonical,ccds=args.ccds,dbNSFP=args.dbNSFP,dbscSNV=args.dbscSNV,distance=args.distance,domains=args.domains,failed=args.failed,hgvs=args.hgvs,mane=args.mane,merged=args.merged,minimal=args.minimal,
mirna=args.mirna,mutfunc=args.mutfunc,numbers=args.numbers,protein=args.protein,refseq=args.refseq,shift_3prime=args.shift_3prime,shift_genomic=args.shift_genomic,transcript_id=args.transcript_id,transcript_version=args.transcript_version,tsl=args.tsl,uniprot=args.uniprot,variant_class=args.variant_class,vcf_string=args.vcf_string,xref_refseq=args.xref_refseq))
elif args.command == "vep_id":
    pprint.pprint(_vep_id(args.id,species=args.species,format=args.format,AncestralAllele=args.AncestralAllele,Blosum62=args.Blosum62,CADD=args.CADD,Conservation=args.Conservation,DisGeNET=args.DisGeNET,EVE=args.EVE,GO=args.GO,GeneSplicer=args.GeneSplicer,IntAct=args.IntAct,LoF=args.LoF,Mastermind=args.Mastermind,MaxEntScan=args.MaxEntScan,
NMD=args.NMD,Phenotypes=args.Phenotypes,SpliceAI=args.SpliceAI,UTRAnnotator=args.UTRAnnotator,appris=args.appris,canonical=args.canonical,ccds=args.ccds,dbNSFP=args.dbNSFP,dbscSNV=args.dbscSNV,distance=args.distance,domains=args.domains,failed=args.failed,hgvs=args.hgvs,mane=args.mane,merged=args.merged,minimal=args.minimal,
mirna=args.mirna,mutfunc=args.mutfunc,numbers=args.numbers,protein=args.protein,refseq=args.refseq,shift_3prime=args.shift_3prime,shift_genomic=args.shift_genomic,transcript_id=args.transcript_id,transcript_version=args.transcript_version,tsl=args.tsl,uniprot=args.uniprot,variant_class=args.variant_class,vcf_string=args.vcf_string,xref_refseq=args.xref_refseq))
elif args.command == "vep_region_get":
    pprint.pprint(_vep_region_get(args.region,args.allele,species=args.species,format=args.format,AncestralAllele=args.AncestralAllele,Blosum62=args.Blosum62,CADD=args.CADD,Conservation=args.Conservation,DisGeNET=args.DisGeNET,EVE=args.EVE,GO=args.GO,GeneSplicer=args.GeneSplicer,IntAct=args.IntAct,LoF=args.LoF,Mastermind=args.Mastermind,MaxEntScan=args.MaxEntScan,
NMD=args.NMD,Phenotypes=args.Phenotypes,SpliceAI=args.SpliceAI,UTRAnnotator=args.UTRAnnotator,appris=args.appris,canonical=args.canonical,ccds=args.ccds,dbNSFP=args.dbNSFP,dbscSNV=args.dbscSNV,distance=args.distance,domains=args.domains,failed=args.failed,hgvs=args.hgvs,mane=args.mane,merged=args.merged,minimal=args.minimal,
mirna=args.mirna,mutfunc=args.mutfunc,numbers=args.numbers,protein=args.protein,refseq=args.refseq,shift_3prime=args.shift_3prime,shift_genomic=args.shift_genomic,transcript_id=args.transcript_id,transcript_version=args.transcript_version,tsl=args.tsl,uniprot=args.uniprot,variant_class=args.variant_class,vcf_string=args.vcf_string,xref_refseq=args.xref_refseq))
elif args.command == "vep_region_post":
#     pprint.pprint(_vep_region_post(args.variants,species=args.species,format=args.format,AncestralAllele=args.AncestralAllele,Blosum62=args.Blosum62,CADD=args.CADD,Conservation=args.Conservation,DisGeNET=args.DisGeNET,EVE=args.EVE,GO=args.GO,GeneSplicer=args.GeneSplicer,IntAct=args.IntAct,LoF=args.LoF,Mastermind=args.Mastermind,MaxEntScan=args.MaxEntScan,
# NMD=args.NMD,Phenotypes=args.Phenotypes,SpliceAI=args.SpliceAI,UTRAnnotator=args.UTRAnnotator,appris=args.appris,canonical=args.canonical,ccds=args.ccds,dbNSFP=args.dbNSFP,dbscSNV=args.dbscSNV,distance=args.distance,domains=args.domains,failed=args.failed,hgvs=args.hgvs,mane=args.mane,merged=args.merged,minimal=args.minimal,
# mirna=args.mirna,mutfunc=args.mutfunc,numbers=args.numbers,protein=args.protein,refseq=args.refseq,shift_3prime=args.shift_3prime,shift_genomic=args.shift_genomic,transcript_id=args.transcript_id,transcript_version=args.transcript_version,tsl=args.tsl,uniprot=args.uniprot,variant_class=args.variant_class,vcf_string=args.vcf_string,xref_refseq=args.xref_refseq))
    pprint.pprint(_vep_region_post(args.region,species=args.species,format=args.format))
elif args.command == "ga4gh_beacon":
    pprint.pprint(_ga4gh_beacon(format=args.format))
elif args.command == "ga4gh_beacon_query":
    pprint.pprint(_ga4gh_beacon_query(args.alternateBases,args.assemblyId,args.referenceBases,args.referenceName,args.start,end=args.end,endMax=args.endMax,endMin=args.endMin,startMax=args.startMax,startMin=args.startMin,variantType=args.variantType,
                        datasetIds=args.datasetIds,includeDatasetResponses=args.includeDatasetResponses,format=args.format))
elif args.command == "ga4gh_features":
    pprint.pprint(_ga4gh_features(args.id,format=args.format))
elif args.command == "ga4gh_features_search":
    pprint.pprint(_ga4gh_features_search(end=args.end,referenceName=args.referenceName,start=args.start,featureTypes=args.featureTypes,featureSetId=args.featureSetId,pageSize=args.pageSize,pageToken=args.pageToken,parentId=args.parentId,format=args.format))
elif args.command == "ga4gh_callsets":
    pprint.pprint(_ga4gh_callsets(args.id,format=args.format))
elif args.command == "ga4gh_datasets_search":
    pprint.pprint(_ga4gh_datasets_search(pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_callsets_search":
    pprint.pprint(_ga4gh_callsets_search(variantSetId=args.variantSetId,name=args.name,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_datasets":
    pprint.pprint(_ga4gh_datasets(args.id,format=args.format))
elif args.command == "ga4gh_featuresets_search":
    pprint.pprint(_ga4gh_featuresets_search(datasetId=args.datasetId,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_featuresets":
    pprint.pprint(_ga4gh_featuresets(args.id,format=args.format))
elif args.command == "ga4gh_variants":
    pprint.pprint(_ga4gh_variants(args.id,format=args.format))
elif args.command == "ga4gh_variants_search":
    pprint.pprint(_ga4gh_variants_search(variantSetId=args.variantSetId,referenceName=args.referenceName,start=args.start,end=args.end,callSetIds=args.callSetIds,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_variantannotations_search":
    pprint.pprint(_ga4gh_variantannotations_search(variantAnnotationSetId=args.variantAnnotationSetId,effects=args.effects,end=args.end,pageSize=args.pageSize,pageToken=args.pageToken,referenceId=args.referenceId,referenceName=args.referenceName,start=args.start,format=args.format))
elif args.command == "ga4gh_variantsets_search":
    pprint.pprint(_ga4gh_variantsets_search(datasetId=args.datasetId,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_variantsets":
    pprint.pprint(_ga4gh_variantsets(args.id,format=args.format))
elif args.command == "ga4gh_references_search":
    pprint.pprint(_ga4gh_references_search(referenceSetId=args.referenceSetId,accession=args.accession,md5checksum=args.md5checksum,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_references":
    pprint.pprint(_ga4gh_references(args.id,format=args.format))
elif args.command == "ga4gh_referencesets_search":
    pprint.pprint(_ga4gh_referencesets_search(accession=args.accession,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_referencesets":
    pprint.pprint(_ga4gh_referencesets(args.id,format=args.format))
elif args.command == "ga4gh_variantannotationsets_search":
    pprint.pprint(_ga4gh_variantannotationsets_search(variantSetId=args.variantSetId,pageSize=args.pageSize,pageToken=args.pageToken,format=args.format))
elif args.command == "ga4gh_variantannotationsets":
    pprint.pprint(_ga4gh_variantannotationsets(args.id,format=args.format))
elif args.command == "info_genomes_taxonomy":
    pprint.pprint(_info_genomes_taxonomy(args.taxon_name,expand=args.expand,format=args.format))
