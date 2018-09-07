#!/usr/bin/env python3

import sys

dx_fh = open(sys.argv[1])
exc_file = open(sys.argv[2])
dna_sheet = open(sys.argv[3])
cnv_dir = sys.argv[4]
maf_dir = sys.argv[5]
mega_sample_sheet = open(sys.argv[6])
header = '#version 2.4\nHugo_Symbol\tEntrez_Gene_Id\tCenter\tChromosome\tStart_Position\tEnd_Position\tStrand' \
         '\tVariant_Classification\tVariant_Type\tReference_Allele\tTumor_Seq_Allele1\tTumor_Seq_Allele2\tdbSNP_RS' \
         '\tdbSNP_Val_Status\tTumor_Sample_Barcode\tMatched_Norm_Sample_Barcode\tMatch_Norm_Seq_Allele1' \
         '\tMatch_Norm_Seq_Allele2\tTumor_Validation_Allele1\tTumor_Validation_Allele2\tMatch_Norm_Validation_Allele1' \
         '\tMatch_Norm_Validation_Allele2\tVerification_Status\tValidation_Status\tMutation_Status\tSequencing_Phase' \
         '\tSequence_Source\tValidation_Method\tScore\tBAM_File\tSequencer\tTumor_Sample_UUID' \
         '\tMatched_Norm_Sample_UUID\tHGVSc\tHGVSp\tHGVSp_ShortTranscript_ID\tExon_Number\tt_depth\tt_ref_count' \
         '\tt_alt_count\tn_depth\tn_ref_count\tn_alt_count\tall_effects\tAllele\tGene\tFeature\tFeature_type' \
         '\tConsequencecDNA_position\tCDS_position\tProtein_position\tAmino_acids\tCodons\tExisting_variation' \
         '\tALLELE_NUM\tDISTANCE\tSTRAND_VEP\tSYMBOL\tSYMBOL_SOURCE\tHGNC_ID\tBIOTYPE\tCANONICAL\tCCDS\tENSP' \
         '\tSWISSPROT\tTREMBL\tUNIPARC\tRefSeq\tSIFT\tPolyPhen\tEXON\tINTRON\tDOMAINS\tAF\tAFR_AF\tAMR_AF\tASN_AF' \
         '\tEAS_AF\tEUR_AF\tSAS_AF\tAA_AF\tEA_AF\tCLIN_SIG\tSOMATIC\tPUBMED\tMOTIF_NAME\tMOTIF_POS\tHIGH_INF_POS' \
         '\tMOTIF_SCORE_CHANGE\tIMPACT\tPICK\tVARIANT_CLASS\tTSL\tHGVS_OFFSETPHENO\tMINIMISED\tExAC_AF\tExAC_AF_AFR' \
         '\tExAC_AF_AMR\tExAC_AF_EAS\tExAC_AF_FIN\tExAC_AF_NFE\tExAC_AF_OTH\tExAC_AF_SAS\tGENE_PHENO\tFILTER' \
         '\tflanking_bps\tvariant_id\tvariant_qual\tExAC_AF_Adj\tExAC_AC_AN_Adj\tExAC_AC_AN\tExAC_AC_AN_AFR' \
         '\tExAC_AC_AN_AMR\tExAC_AC_AN_EAS\tExAC_AC_AN_FIN\tExAC_AC_AN_NFE\tExAC_AC_AN_OTH\tExAC_AC_AN_SAS' \
         '\tExAC_FILTER\tgnomAD_AF\tgnomAD_AFR_AF\tgnomAD_AMR_AF\tgnomAD_ASJ_AF\tgnomAD_EAS_AF\tgnomAD_FIN_AF' \
         '\tgnomAD_NFE_AF\tgnomAD_OTH_AF\tgnomAD_SAS_AF'
dx_dict = {}
maf_fh = {}
cnv_fh = {}
blacklist = {}
next(dx_fh)
for line in dx_fh:
    info = line.rstrip('\n').split('\t')
    cbttc_dx = info[0]
    cbio_short = info[1]
    dx_dict[cbttc_dx] = cbio_short
    maf_fh[cbio_short] = open(cbio_short + '.strelka.vep.filtered.maf', 'w')
    cnv_fh[cbio_short] = open(cbio_short + '.predicted_cnv.txt', 'w')
    maf_fh[cbio_short].write(header)

dx_fh.close()

for line in exc_file:
    blacklist[line.rstrip('\n')] = 0

maf_exc = {"Silent": 0, "Intron": 0, "IGR": 0, "3'UTR": 0, "5'UTR": 0, "3'Flank": 0, "5'Flank": 0}

dna_task_dict = {}
next(dna_sheet)
for line in dna_sheet:
    info = line.rstrip('\n').split('\t')
    if info[2] not in blacklist:
        dna_task_dict[info[2]] = info[-2]