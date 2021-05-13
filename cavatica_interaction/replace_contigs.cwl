cwlVersion: v1.0
class: CommandLineTool
id: replace_contigs
doc: >-
  This tool will run a Python script that replaces contigs in a vcf 
  with contigs from another vcfs in the header
requirements:
  - class: DockerRequirement
    dockerPull: 'pgc-images.sbgenomics.com/d3b-bixu/consensus-merge:1.1.0'
  - class: InlineJavascriptRequirement
  - class: InitialWorkDirRequirement
    listing:
    - entryname: replace_contigs.py
      entry:
        $include: ../cavatica_interaction/replace_contigs.py
  - class: ResourceRequirement
    ramMin: 1000
    coresMin: 1
  - class: ShellCommandRequirement
arguments:
  - position: 0
    shellQuote: false
    valueFrom: >-
      python replace_contigs.py
      --example_vcf $(inputs.example_vcf.path)
      --input_vcf $(inputs.input_vcf.path) &&
      bgzip $(inputs.input_vcf.nameroot) &&
      tabix $(inputs.input_vcf.basename)

inputs:
  example_vcf: { type: File, doc: "VCF with contigs you want to use" }
  input_vcf: { type: File, doc: "VCF with contigs that need to be replaced" }
outputs: 
  reheadered:
    type: File
    outputBinding:
      glob: "*.vcf.gz"
    secondaryFiles: ['.tbi']