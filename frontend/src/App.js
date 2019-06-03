import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Chart from "react-apexcharts";

class App extends Component {
  state = {
        posts: [],
        options: {
            chart: {
              id: "basic-bar"
            },
            xaxis: {
              categories: this.time
            }
        },
        series: [
            {
              name: "temperature",
              data: []
            },
            {
                name: "humidity",
                data: []
              }
        ]
  };

  async componentDidMount() {
      try {
        //   let time, temperature, humidity;
        
          const res = await fetch('http://127.0.0.1:8000/api/');
          const posts = await res.json();
          this.time = [];
          let temperature = [], humidity = [];
          const newSeries = [];
          let newOptions = {};

          posts.map(i => {
              this.time.push(i.time);
              temperature.push(i.temperature);
              humidity.push(i.humidity);   
          });
          console.log(this.time)
          console.log(temperature);
          console.log(humidity);

          newSeries.push({name: 'temerature', data: temperature});
          newSeries.push({name: 'humidity', data: humidity});
          console.log(this.time);
        //   newOptions = this.state.options;
        //   newOptions.xaxis.categories = this.time;
        //   console.log(newOptions)
        //   console.log(newOptions.xaxis.categories);

          this.setState({
              posts,
              series: newSeries,
            //   options: newOptions
          });
      } catch (e) {
          console.log(e);
      }
  }


  render() {
      return (
        <>  
            <div className="row">
                <div className="mixed-chart">
                    <Chart
                        options={this.state.options}
                        series={this.state.series}
                        type="line"
                        width="500"
                    />
                </div>
            </div>
            <div>
                {this.state.posts.map(item => (
                    <div key={item.time}>
                        <h1>Time {item.time}</h1>
                        <p>Temperature <span>{item.temperature}</span></p>
                        <p>Humidity <span>{item.humidity}</span></p>
                    </div>
                ))}
            </div>
        </>
      );
  }
}

/* <div>
                  <Table>
                      <TableHead>
                          <TableRow>
                              <TableCell>번호</TableCell>
                              <TableCell>데이터</TableCell>
                          </TableRow>
                      </TableHead>
                      <TableBody>
                          {this.state.posts.map(item => (<Customer key={item.id} number={item.number} data={item.data}/>))}
                      </TableBody>
                  </Table>
              </div> */

// function App() {
//   return (
//     <>
//       <div className="App">
//         <header className="App-header">
//           <img src={logo} className="App-logo" alt="logo" />
//           <p>
//             Edit <code>src/App.js</code> and save to reload.
//           </p>
//           <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Learn React
//           </a>
//         </header>
//       </div>
//     </>
//   );
// }

export default App;
