from Bio.Seq import Seq

def coarse_filtering(reads, opts, template_kmers, flanking_sequences):
    recruitedReads = []
    template_set = set([kmer for value in template_kmers.values() for kmer in value])
    skipped_reads = 0
    for j, record in enumerate(reads):
        sequence = record.seq
        quality = record.letter_annotations["phred_quality"]

        if j == 0:
            read_length = len(sequence)

        #Generate k-splits
        reads = [sequence[n:n+opts.k] for n in range(0, read_length-opts.k+1, opts.k)]

        if j == 0:
            k_splits_per_read = len(reads)
        
        for i, read in enumerate(reads):
            
            #Throw away low quality sections of the read and record the number of disposals.
            avg_qual = sum(quality[i*opts.k:(i*opts.k)+opts.k])/opts.k
            if avg_qual < opts.q:
                skipped_reads += 1
                continue
            
            # Forward
            readSeq = str(read)
            if readSeq in template_set or readSeq in flanking_sequences:
                recruitedReads.append(readSeq)
          

    #Nucleotides seen takes into account number of reads, read length and skipped read sections
    nucleotides_seen = (j+1)*k_splits_per_read-skipped_reads
    return(nucleotides_seen, recruitedReads)
