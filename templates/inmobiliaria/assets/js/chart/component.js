// alert('adad');
a=new Vue({
	el: '#isDiv',
	data: {
		gerenteOptions: [
			'ventas logradas',
			'alquileres gestionados'
		],
		selectOptions: [
			{text: 'Total', value: 'T'},
			{text: 'Ventas', value: 'V'},
			{text: 'Subastas', value: 'S'},
			{text: 'Alquiler', value: 'A'},
			{text: 'Todo', value: 'TT'}	
		],
		monthOptions: [
			{text: 'Anual',		value: 0},
			{text: 'Enero', 	value: 1},
			{text: 'Febrero', 	value: 2},
			{text: 'Marzo', 	value: 3},
			{text: 'Abril', 	value: 4},
			{text: 'Mayo', 		value: 5},
			{text: 'Junio', 	value: 6},
			{text: 'Julio', 	value: 7},
			{text: 'Agosto', 	value: 8},
			{text: 'Septiembre',value: 9},
			{text: 'Octubre', 	value: 10},
			{text: 'Noviembre', value: 11},
			{text: 'Diciembre', value: 12}
		],
		typeOptions: [
			'line',
			'bar'
		],
		localeOptions: [
			{text: 'Cuartos', value: 'R'},
			{text: 'Casas', value: 'H'},
			{text: 'Todo', value: 'T'}
		],
		opcion_gerente: 'ventas logradas',
		modo_gerente: 'false',
		selected: 'T',
		myGraph: {},
		type: 'bar',
		year: 2018,
		month: 0,	//INSERTADOS O REALIZADOS
		acum_temp: '0',
		published: 'true',
		locale: 'R',
		datasets: {
			}
	},
	template: `
		<div>
	        <canvas id="total"></canvas>
			<div class='text-center'>
				<div class="btn-group">
					<button class="btn btn-default" v-on:click='changeYear(-1)'>Anterior</button>
					<button class="btn btn-default" style='width:150px;' disabled>{{year}}</button>
					<button class="btn btn-default" v-on:click='changeYear(1)'>Siguiente</button>
				</div>
			</div>
			<div class='text-center'>
				<div class="btn-group">
					<button class="btn btn-default" v-on:click='changeMonth(-1)'>Anterior</button>
					<button class="btn btn-default" style='width:150px;' disabled>{{monthOptions[month].text}}</button>
					<button class="btn btn-default" v-on:click='changeMonth(1)'>Siguiente</button>
				</div>
			</div>
			
			<!-- <span>Selected: {{ selected }}</span> -->
			<!-- <button v-on:click='loadGraph'>Load Graph</button> -->
	        <div>
		        <input type="radio" id="one" value="0" v-model="acum_temp">
				<label for="one">Acumulado</label>
				<input type="radio" id="two" value="1" v-model="acum_temp">
				<label for="two">Temporal</label>
	        </div>
	        <input type='checkbox' v-model='published'>
	        <select v-model="selected">
			  <option v-for="opt in selectOptions" v-bind:value='opt.value'>{{opt.text}}</option>
			</select>
			<select v-model="locale">
			  <option v-for="opt in localeOptions" v-bind:value='opt.value'>{{opt.text}}</option>
			</select>
			<select v-model="type">
			  <option v-for="typee in typeOptions" v-bind:value='typee'>{{typee}}</option>
			</select>

			<div>
			<input type='checkbox' v-model='modo_gerente'>
			<label for="one">Gerentes</label>
			</div>
	
			<div>
			<select v-model="opcion_gerente">
			<option v-for="opx in gerenteOptions" v-bind:value='opx'>{{opx}}</option>
			</select>
			</div>
		</div>
		
	`,

	mounted: function(){
		today = new Date()
		this.year = today.getFullYear()
		this.month = 0//today.getMonth()
		// this.changeLabel()
		that = this

		this.$watch(vm => [vm.selected, vm.year, vm.month,vm.modo_gerente,vm.opcion_gerente].join(), val => {
		  that.loadGraph()
		})
		var ctx = document.getElementById("total").getContext("2d");

		// configTotal = {}
		$.post("/graph",
			    {
					modo_gerente: that.modo_gerente,
					opcion_gerente: that.opcion_gerente,
			        info:  that.selected,
			        year:  that.year,
			        month: that.month,
			        mode:  that.acum_temp,
			        type:  that.published,
			        locale:that.locale
			    },
			    function(data, status){
			    	// that.datasets = data.data.datasets
			    	config = {
				        type: 'bar',
				        data: {
				            labels: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
				        },
				        options: {
				            responsive: true,
				            title:{
				                display: true,
				                text:'Informe de inmuebles anual',
				                fontSize: 20
				            },
				            tooltips: {
				                mode: 'index',
				                intersect: false,
				            },
				            hover: {
				                mode: 'nearest',
				                intersect: true
				            },
				            scales: {
				                xAxes: [{
				                    // stacked: true,
				                    display: true,
				                    scaleLabel: {
						                fontSize: 16,
				                        display: true,
				                        labelString: 'Meses'
				                    }
				                }],
				                yAxes: [{
				                    display: true,
				                    scaleLabel: {
						                fontSize: 16,
				                        display: true,
				                        labelString: 'Valor'
				                    }
				                }]
				            }
				        }
					}
					console.log('hola' + data.datasets)
				    config.data.datasets = data.datasets
			    	that.myGraph = new Chart(ctx, config)
			    });
	},
	watch: {
		modo_gerente: function(){
			this.loadGraph()
		},
		acum_temp: function(){
			this.loadGraph()
		},
		type: function(){
			this.myGraph.config.type=this.type
			this.myGraph.update()
		},
		locale: function(){
			this.loadGraph()
		},
		published: function(){
			this.loadGraph()
		}
	},
	methods: {
		changeYear: function(val){
			this.year+=val
			this.changeLabel()
		},
		changeMonth: function(val){
			this.month+=val
			if(this.month==-1){
				this.month=12
			}
			else if(this.month==13){
				this.month=0
			}
			this.changeLabel()
		},
		changeLabel: function(names)
		{
			if(this.month != '0')
			{
				daysCount = [0,31, (!(this.year&3||this.year&15&&!(this.year%25)) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][this.month];
				var days = []
				for (var i = 1; i <= daysCount; i++) {
				   days.push(i);
				}
				this.myGraph.config.data.labels = days.slice(0,this.myGraph.config.data.datasets[0].data.length)
				
			}
			else
			{
				this.myGraph.config.data.labels = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
			}
			this.myGraph.update()
			
		},
		loadGraph: function(){
			that = this
			$.post("/graph",
			    {
					modo_gerente: that.modo_gerente,
					opcion_gerente: that.opcion_gerente,
			        info:  that.selected,
			        year:  that.year,
			        month: that.month,
			        mode:  that.acum_temp,
			        type:  that.published,
			        locale:that.locale
			    },
			    function(data, status){
		    		individual = false
			    	if(data.hasOwnProperty('datasets')){
			    		individual = true
			    		that.myGraph.data.datasets = data.datasets
			    	}
			    	if(data.hasOwnProperty('xLabel')){
			    		individual = true
			    		that.myGraph.config.data.labels = data.xLabel
			    	}
			    	if(data.hasOwnProperty('title')){
			    		individual = true
			    		that.myGraph.config.options.title.text = data.title
			    	}
			    	if(data.hasOwnProperty('type')){
			    		individual = true
			    		that.myGraph.config.type = data.type
			    	}
			    	if(data.hasOwnProperty('xAxes_stacked')){
			    		individual = true
			    		that.myGraph.config.options.scales.xAxes[0].stacked = data.xAxes_stacked
			    	}
			    	if(data.hasOwnProperty('yAxes_stacked')){
			    		individual = true
			    		that.myGraph.config.options.scales.yAxes[0].stacked = data.yAxes_stacked
			    	}
			    	if(data.hasOwnProperty('labels')){
			    		individual = true
			    		that.myGraph.config.data.labels = data.labels
			    	}
			    	if(individual==false){
				    	that.myGraph.config = data
			    	}
					that.myGraph.update()
			    });
		}
	}
})

Vue.component('auction',{
	data: function(){
		return {
			current: 0,
			total: 0,
			interval: null,
			intervalRate: 200,
			refreshData: null,
			refreshDataInterval: 10000,
			previousActions: [],
			price: 0,
			minPrice: 0,
			progressBarStyle: ['progress-bar','progress-bar-striped','active']
		}
	},
	props: ['id'],
	computed:{
		styles: function(){
			return {width: this.percent+'%', 'font-size':'20px', height: '30px'}
		},
		getHours: function(){
			return Math.floor(((this.current/1000)/60)/60)
		},
		getMinutes: function(){
			return Math.floor((this.current/1000)/60)
		},
		getSeconds: function(){
			sec = Math.floor((this.current/1000)%60)
			return sec>9?sec:'0'+sec
		},
		getTime: function(){
			result = this.getSeconds
			if(this.getMinutes>0){
				result = this.getMinutes%60+':'+ result
				if(this.getHours>0){
					result = this.getHours%60 + ':'+ result
					if(this.getHours>60){
						result = Math.floor(this.getHours/24) + ' dias ' + result
					}
				}
			}
			return result
		},
		percent: function(){
			return (this.current/this.total*100)
		},
		getProgressBarColor: function(){
			classColor = ''
			if(this.percent>30)
				classColor = ''
			else if(this.percent>20)
				classColor = 'progress-bar-info'
			else if(this.percent>10)
				classColor = 'progress-bar-warning'
			else
				classColor = 'progress-bar-danger'
			return classColor
		}
	},
	mounted: function(){
		that = this
		this.getData(true)
		setInterval(()=>that.getData(false),this.refreshDataInterval)
		// this.price=this.minPrice

		this.interval = setInterval(function(){
			// that.current=that.current-that.intervalRate
			that.current=Math.max(that.current-that.intervalRate,0)
			if(that.current<0)
				that.current=that.total 
			},this.intervalRate)

	},
	template: `
		<div>
			<div class="progress" style="height: 30px">
	    		<div v-bind:class="[progressBarStyle,getProgressBarColor]" role="progressbar" v-bind:aria-valuenow="current" aria-valuemin="0" v-bind:aria-valuemax="total" v-bind:style='styles'>
		      		{{getTime}}
			  	</div>
			</div>
			<div class='text-center'>
				<table class='table' style='width: 200px; margin: auto'>
					<thead>
						<th>Usuario</th>
						<th>Cantidad</th>
					</thead>
					<tbody>
						<tr v-for='auction in previousActions'>
							<td>{{auction.name}}</td>
							<td>{{auction.price}}</td>
						</tr>
					</tbody>
				</table>
				<form action='/realizarPuja' method='POST'>
					<input v-model='price' name='price' type='number'>
					<input v-model='id' type='hidden' name='id'>
					<input type="submit" value='Realizar Puja'/>
				</form>
			</div>
		</div>
		`
	,
	methods: {
		stop: function(){
			clearInterval(this.click)
		},
		clicking: function(value){
			that = this
			this.click = setInterval(()=>that.price+=value,10)
		},
		setTotalSeconds: function(value){
			this.total=value*1000
		},
		setCurrentSeconds: function(value){
			this.current = Math.min(value*1000,this.total)
		},
		getData: function(firstTime){
			that = this
			$.post
			("/getTime",
			    {
			        id: that.id
			    },
			    function(data, status){
					if(data.hasOwnProperty('url'))
						location.href = data.url
			    	// begin
			    	// end
			    	// previousActions
					data.end = (new Date(data.end)).getTime()
					data.begin = (new Date(data.begin)).getTime()
					that.total = Number(data.end) - Number(data.begin)
		    		now = Math.floor(new Date().getTime())
					console.log(data.begin)
					console.log(now)
					console.log(data.end)
		    		that.current = Number(data.end) - now
		    		// Si pasan segundos, en vez de milisegundos
		    		// that.total*=1000
		    		// that.current*=1000
		    		that.previousActions = data.previousActions
		    		that.minPrice = data.length>0 ? Number(data.previousActions[0].price)+1 : 0
		    		if(firstTime) that.price = that.minPrice
			    });

		}
	},
	filters: {
		createTime: function(value){
			return value + ' s'
		}
	}
});
new Vue({
	el: '#auctionDiv'
});
