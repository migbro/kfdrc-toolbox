cwlVersion: v1.0
class: CommandLineTool
id: bam_file_subset
label: Subset bam file
doc: Utility to subset an existing bam for testing purposes
requirements:
  - class: InlineJavascriptRequirement
  - class: ShellCommandRequirement
  - class: DockerRequirement
    dockerPull: 'kfdrc/samtools:1.9'
  - class: ResourceRequirement
    coresMin: 36
baseCommand: [samtools, view]
arguments:
  - position: 1
    shellQuote: false
    valueFrom: >-
      -@ 36 -bhs $(inputs.fraction) $(inputs.input_align.path) > $(inputs.output_bam_basename + ".bam")
inputs:
  input_align: File
  output_bam_basename: string
  fraction: float
outputs:
  output:
    type: File
    outputBinding:
      glob: '*.bam'
    secondaryFiles: [^.bai]
