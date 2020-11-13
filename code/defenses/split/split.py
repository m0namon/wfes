import os
import sys

DEFENDED = './defended'
TIMING = 300 # consistent timing schedule, in milliseconds

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {} <input folder>'.format(sys.argv[1])
        sys.exit(1)
    
    dataset = sys.argv[1]
    outdirectory = DEFENDED
    
    if not os.path.exists(outdirectory):
        os.makedirs(outdirectory)

    traces = {}

    # Defend
    for fname in os.listdir(dataset):
        # Skip open world traces
        if '-' not in fname:
            continue
        print fname,
        site_id = fname[0:fname.find('-')]
        if site_id not in traces:
            traces[site_id] = 0
        infname = os.path.join(dataset, fname)
        outfname = os.path.join(outdirectory, fname)

        packets = []
        with open(infname, 'r') as f:
            for x in f.readlines():
                t, s = x.split('\t')
                t = float(t) * 1000.0   # To milliseconds
                s = int(s)
                packets.append((t, s))
        last_packet = 0
        last_packet_time = 0
        for i, packet in enumerate(packets):
            time, _ = packet
            if time - last_packet_time > TIMING:
                fname = os.path.join(outdirectory, str(site_id) + "-" + str(traces[site_id]))
                with open(fname, "w") as f:
                    for t, s in packets[last_packet:i]:
                        t = t - last_packet_time
                        t /= 1000.0             # To seconds
                        s = 1 if s > 0 else -1
                        f.write(repr(t) + "\t" + repr(s) + "\n")
                last_packet = i
                last_packet_time = time
                traces[site_id] += 1
