import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';
import Chart from "react-apexcharts";
import ImgMediaCard from "./components/ImgMediaCard"

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
              name: "distance",
              data: []
            }
        ]
  };

  async componentDidMount() {
      try {
        //   let time, temperature, humidity;
        
          const res = await fetch('http://ec2-13-124-30-140.ap-northeast-2.compute.amazonaws.com:8080/rssi/serial/');
          const posts = await res.json();
          console.log(posts);
        //   this.id = [];
          let data2 = [];
          const newSeries = [];
          let newOptions = {};

          posts.map(i => {
            //   this.time.push(i.id);
              data2.push(i.data);
          });
          console.log(this.id)
          console.log(data2);

          newSeries.push({name: 'distance', data: data2});
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
            <ImgMediaCard/>
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
