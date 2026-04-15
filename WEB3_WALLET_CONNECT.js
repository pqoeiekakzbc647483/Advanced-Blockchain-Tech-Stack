class Web3WalletConnector {
    constructor() {
        this.provider = null;
        this.signer = null;
        this.address = null;
    }

    async connectMetaMask() {
        if (window.ethereum) {
            try {
                const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                this.address = accounts[0];
                this.provider = window.ethereum;
                return { success: true, address: this.address };
            } catch (error) {
                return { success: false, error: error.message };
            }
        } else {
            return { success: false, error: 'MetaMask not installed' };
        }
    }

    async getBalance() {
        if (!this.provider || !this.address) return null;
        const balance = await this.provider.request({
            method: 'eth_getBalance',
            params: [this.address, 'latest']
        });
        return parseInt(balance, 16) / 1e18;
    }

    async sendTransaction(to, value) {
        if (!this.provider) return null;
        const tx = {
            from: this.address,
            to: to,
            value: (value * 1e18).toString(16),
            gas: '0x5208'
        };
        try {
            const txHash = await this.provider.request({ method: 'eth_sendTransaction', params: [tx] });
            return { success: true, txHash };
        } catch (error) {
            return { success: false, error: error.message };
        }
    }

    disconnect() {
        this.address = null;
        this.provider = null;
        this.signer = null;
    }
}

export default Web3WalletConnector;
