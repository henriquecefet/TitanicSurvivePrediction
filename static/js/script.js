new Vue({
    el: '#app',
    data: {
        formData: {
            Sex: '',
            Embarked: '',
            Pclass: '',
            Age: '',
            Fare: ''
        },
        prediction: "<p>Make a prediction</P>"
    },
    methods: {
        replaceComma(field) {
            this.formData[field] = this.formData[field].replace(',', '.');
          },
        submitForm() {
            fetch('http://127.0.0.1:5000/predict', { // Use o endereço correto da sua API aqui
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                if (data.prediction === 1) {
                    console.log("Probably Survived");
                    this.prediction = `<p style="color: green;">Provavelmente sobreviveu</p>`;
                } else if (data.prediction === 0) {
                    console.log("Unfortunally, probably died");
                    this.prediction = `<p style="color: red;">Inferlizmente, provavelmente faleceu</p>`;
                } else {
                    this.prediction = `<p>Unexpected response from server</p>`;
                    console.log("Unexpected response from server"); 

                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Algo deu errado");
            });
        }
    }
});



