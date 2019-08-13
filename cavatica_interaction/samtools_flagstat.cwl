cwlVersion: v1.0
class: CommandLineTool
id: samtools_flagstat_bam
label: Get bam flagstats
doc: Utility get flagstat of a bam file
requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.9'
  - class: ResourceRequirement
    coresMin: 36
baseCommand: [samtools, flagstat]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      -@ 36 $(inputs.input_align.path) > $(inputs.input_align.nameroot).flagstat
inputs:
  input_align: File
  reference: {type: File, secondaryFiles: [.fai]}
outputs:
  output:
    type: File
    outputBinding:
      glob: '*.flagstat'
