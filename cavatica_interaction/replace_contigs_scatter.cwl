cwlVersion: v1.0
class: Workflow
id: ngs_checkmate_wf
doc: "A wrapper workflow to reheader VCF files in bulk"
requirements:
  - class: ScatterFeatureRequirement
  - class: MultipleInputFeatureRequirement
inputs:
  example_vcf: { type: File, doc: "VCF with proper contigs in header" }
  input_vcfs: { type: 'File[]', doc: "VCFs to update contigs. HIGHLY RECOMMEND PUTTING THEM IN THEIR OWN DIRECTORY"}
outputs: 
  reheadered: { type: 'File[]', outputSource: reheader_vcf/reheadered }
steps:
  reheader_vcf:
    run: replace_contigs.cwl
    in:
      example_vcf: example_vcf
      input_vcf: input_vcfs
    scatter: [input_vcf]
    out: [reheadered]
$namespaces:
  sbg: https://sevenbridges.com
hints:
  - class: 'sbg:AWSInstanceType'
    value: c5.4xlarge
  - class: 'sbg:maxNumberOfParallelInstances'
    value: 4