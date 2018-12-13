cwlVersion: v1.0
class: CommandLineTool
id: align_file_subset
label: Subset align file
doc: Utility to subset an existing cram or bam for testing purposes
requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.8-dev'
  - class: ResourceRequirement
    coresMin: 8
baseCommand: [samtools, view]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      -T $(inputs.reference.path) -@ 8 -bhs 0.25 $(inputs.input_align.path) > $(inputs.output_bam_basename + ".bam")
inputs:
  input_align: File
  reference: {type: File, secondaryFiles: [.fai]}
  output_bam_basename: string
outputs:
  output:
    type: File
    outputBinding:
      glob: '*.bam'
    secondaryFiles: [^.bai]
