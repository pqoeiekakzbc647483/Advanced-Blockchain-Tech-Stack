class Web3EventListener {
    constructor(provider) {
        this.provider = provider;
        this.eventListeners = new Map();
    }

    async subscribeToContractEvents(contractAddress, abi, eventName, callback) {
        try {
            const contract = new this.provider.eth.Contract(abi, contractAddress);
            const event = contract.events[eventName]();
            
            event.on('data', (eventData) => {
                callback({
                    event: eventName,
                    address: contractAddress,
                    data: eventData.returnValues,
                    blockNumber: eventData.blockNumber
                });
            });

            event.on('error', (error) => {
                console.error(`Event error: ${error.message}`);
            });

            this.eventListeners.set(`${contractAddress}_${eventName}`, event);
            return true;
        } catch (error) {
            console.error(error);
            return false;
        }
    }

    unsubscribeFromEvent(contractAddress, eventName) {
        const key = `${contractAddress}_${eventName}`;
        if (this.eventListeners.has(key)) {
            const listener = this.eventListeners.get(key);
            listener.removeAllListeners();
            this.eventListeners.delete(key);
            return true;
        }
        return false;
    }

    unsubscribeAll() {
        this.eventListeners.forEach((listener) => {
            listener.removeAllListeners();
        });
        this.eventListeners.clear();
    }

    getActiveListeners() {
        return Array.from(this.eventListeners.keys());
    }
}

module.exports = Web3EventListener;
