cwlVersion: v1.0
class: CommandLineTool
id: bam_file_index
label: Index bam file
doc: Utility to index an existing bam
requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.9'
  - class: ResourceRequirement
    coresMin: 16
baseCommand: [samtools, index]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      -@ 16 $(inputs.input_align.path) $(inputs.input_align.nameroot).bai
inputs:
  input_align: File
outputs:
  output:
    type: File
    outputBinding:
      glob: '*.bai'
