(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{12:function(e,t,n){e.exports=n(28)},17:function(e,t,n){},19:function(e,t,n){e.exports=n.p+"static/media/logo.ee7cd8ed.svg"},20:function(e,t,n){},28:function(e,t,n){"use strict";n.r(t);var a=n(0),r=n.n(a),i=n(4),o=n.n(i),s=(n(17),n(2)),c=n.n(s),l=n(5),u=n(6),m=n(7),p=n(10),h=n(8),d=n(11),v=(n(19),n(20),n(9)),f=n.n(v),w=function(e){function t(){var e,n;Object(u.a)(this,t);for(var a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];return(n=Object(p.a)(this,(e=Object(h.a)(t)).call.apply(e,[this].concat(r)))).state={posts:[],options:{chart:{id:"basic-bar"},xaxis:{categories:n.time}},series:[{name:"temperature",data:[]},{name:"humidity",data:[]}]},n}return Object(d.a)(t,e),Object(m.a)(t,[{key:"componentDidMount",value:function(){var e=Object(l.a)(c.a.mark(function e(){var t,n,a,r,i,o=this;return c.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.prev=0,e.next=3,fetch("http://127.0.0.1:8000/api/");case 3:return t=e.sent,e.next=6,t.json();case 6:n=e.sent,this.time=[],a=[],r=[],i=[],{},n.map(function(e){o.time.push(e.time),a.push(e.temperature),r.push(e.humidity)}),console.log(this.time),console.log(a),console.log(r),i.push({name:"temerature",data:a}),i.push({name:"humidity",data:r}),console.log(this.time),this.setState({posts:n,series:i}),e.next=24;break;case 21:e.prev=21,e.t0=e.catch(0),console.log(e.t0);case 24:case"end":return e.stop()}},e,this,[[0,21]])}));return function(){return e.apply(this,arguments)}}()},{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"mixed-chart"},r.a.createElement(f.a,{options:this.state.options,series:this.state.series,type:"line",width:"500"}))),r.a.createElement("div",null,this.state.posts.map(function(e){return r.a.createElement("div",{key:e.time},r.a.createElement("h1",null,"Time ",e.time),r.a.createElement("p",null,"Temperature ",r.a.createElement("span",null,e.temperature)),r.a.createElement("p",null,"Humidity ",r.a.createElement("span",null,e.humidity)))})))}}]),t}(a.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));o.a.render(r.a.createElement(w,null),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then(function(e){e.unregister()})}},[[12,1,2]]]);
//# sourceMappingURL=main.2948fc22.chunk.js.map