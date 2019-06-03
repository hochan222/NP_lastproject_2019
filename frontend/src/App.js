import React, {Component} from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  state = {
        posts: []
    };

  async componentDidMount() {
      try {
          const res = await fetch('http://127.0.0.1:8000/api/');
          const posts = await res.json();
          this.setState({
              posts
          });
      } catch (e) {
          console.log(e);
      }
  }


  render() {
      return (
        <>
            <div>
                {this.state.posts.map(item => (
                    <div key={item.time}>
                        <h1>{item.time}</h1>
                        <span>{item.temperature}</span>
                        <span>{item.humidity}</span>
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
