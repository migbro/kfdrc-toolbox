cwlVersion: v1.0
class: CommandLineTool
id: cram_file_subset
label: Subset cram file
doc: Utility to subset an existing cram for testing purposes
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
      -T $(inputs.reference.path) -@ 36 -bhs $(inputs.fraction) -C $(inputs.input_align.path) > $(inputs.output_bam_basename).cram &&
      samtools index $(inputs.output_bam_basename).cram $(inputs.output_bam_basename).cram.crai
inputs:
  input_align: File
  reference: {type: File, secondaryFiles: [.fai]}
  output_bam_basename: string
  fraction: float
outputs:
  output:
    type: File
    outputBinding:
      glob: "$(inputs.output_bam_basename).cram"
    secondaryFiles: [.crai]
