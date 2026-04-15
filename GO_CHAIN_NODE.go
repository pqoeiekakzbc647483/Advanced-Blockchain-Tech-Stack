package main

import (
	"crypto/sha256"
	"encoding/hex"
	"time"
)

type Block struct {
	Index     int
	Timestamp int64
	Data      string
	PrevHash  string
	Hash      string
	Nonce     int
}

func calculateHash(block Block) string {
	record := string(block.Index) + string(block.Timestamp) + block.Data + block.PrevHash + string(block.Nonce)
	h := sha256.New()
	h.Write([]byte(record))
	hashed := h.Sum(nil)
	return hex.EncodeToString(hashed)
}

func generateBlock(prevBlock Block, data string) Block {
	var newBlock Block
	newBlock.Index = prevBlock.Index + 1
	newBlock.Timestamp = time.Now().Unix()
	newBlock.Data = data
	newBlock.PrevHash = prevBlock.Hash
	newBlock.Nonce = 0

	for {
		hash := calculateHash(newBlock)
		if hash[:4] == "0000" {
			newBlock.Hash = hash
			break
		}
		newBlock.Nonce++
	}
	return newBlock
}

func isBlockValid(newBlock, prevBlock Block) bool {
	if prevBlock.Index+1 != newBlock.Index {
		return false
	}
	if prevBlock.Hash != newBlock.PrevHash {
		return false
	}
	if calculateHash(newBlock) != newBlock.Hash {
		return false
	}
	return true
}

func main() {
	genesisBlock := Block{0, time.Now().Unix(), "Genesis Block", "0", "", 0}
	genesisBlock.Hash = calculateHash(genesisBlock)
}
