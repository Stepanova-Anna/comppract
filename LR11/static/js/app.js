const { createApp } = Vue

createApp({
    data() {
        return {
            keyFile: null,
            secretFile: null,
            decryptedText: '',
            error: null
        }
    },
    methods: {
        handleKeyUpload(event) {
            this.keyFile = event.target.files[0];
        },
        handleSecretUpload(event) {
            this.secretFile = event.target.files[0];
        },
        async decrypt() {
            this.error = null;
            this.decryptedText = '';

            if (!this.keyFile) {
                this.error = "Please select a key file.";
                return;
            }
            if (!this.secretFile) {
                this.error = "Please select an encrypted text file.";
                return;
            }

            const formData = new FormData();
            formData.append('key', this.keyFile);
            formData.append('secret', this.secretFile);

            try {
                const response = await axios.post('/decypher', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });
                console.log("Response from server:", response); 
                console.log("Response data:", response.data); 
                this.decryptedText = response.data;
                console.log("Decrypted text (after assignment):", this.decryptedText);
            } catch (error) {
                console.error("Error during decryption:", error);
                if (error.response) {
                    this.error = `Decryption failed: Server error ${error.response.status}: ${error.response.data}`;
                    console.log("Response data:", error.response.data); 
                    console.log("Response status:", error.response.status);
                    console.log("Response headers:", error.response.headers);
                } else if (error.request) {
                    this.error = `Decryption failed: No response from server. Check connection.`;
                } else {
                    this.error = `Decryption failed: ${error.message}. Check key/text or server.`;
                }
            }
        }
    }
}).mount('#app')