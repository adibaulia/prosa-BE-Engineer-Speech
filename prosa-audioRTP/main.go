package main

import (
	"log"
	"os"

	pcap "github.com/Lukasa/gopcap"
)

func main() {
	f, err := os.Open("test_180s.pcap")
	if err != nil {
		log.Printf("could not open the file, cause %v", err)
		return
	}

	r, err := pcap.NewReader(f)
	if err != nil {
		log.Printf("could not create reader, cause %v", err)
		return
	}

	data, ci, err := r.ReadPacketData()
	if err != nil {
		log.Printf("could not read packet data, cause %v", err)
		return
	}
	log.Printf("Ci length %v", ci)

	// if err := ioutil.WriteFile("test.wav", data, os.ModeDir); err != nil {
	// 	log.Printf("could not write data, cause %v", err)
	// }
}
