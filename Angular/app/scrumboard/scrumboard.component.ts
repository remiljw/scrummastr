import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from './../data.service';
import { DragulaService } from 'ng2-dragula';
import { Subscription } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';



@Component({
  selector: 'app-scrumboard',
  templateUrl: './scrumboard.component.html',
  styleUrls: ['./scrumboard.component.css']
})
export class ScrumboardComponent implements OnInit {
  public arrCount =  [1, 2, 3, 4];
  subs = new Subscription();

  constructor(private router: Router, public dataservice: DataService,private dragula:DragulaService, private http : HttpClient) { 
   
    this.dataservice.username = sessionStorage.getItem('username');
    this.dataservice.role = sessionStorage.getItem('role');
    this.dataservice.authOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
      };
    this.http.get('http://127.0.0.1:8080/api/scrumusers/',this.dataservice.httpOptions).subscribe(
    data => {
      console.log(data);
      for(let i = 0; i < data['length']; i++){
        data[i]['scrumygoals_set'] = data[i]['scrumygoals_set'].filter(item => item['visible']);
      }
      this.dataservice.users = data;
    },
    err => {
            this.dataservice.message = 'Unexpected Error';
            console.log(err);
          }
   ); 
    
    this.dragula.createGroup('mainTable',{
      revertOnSpill: true,
      direction: 'horizontal',
      invalid: (el) => {
        return el.id == 'author' || el.id == 'remove' || el.id == 'blank';
      }
    });

    this.subs.add(
      this.dragula.drop('mainTable').subscribe(
        value =>{
          console.log(value);
          var el = value ['el'];
          var target = value ['target'];
          var source = value ['source'];

          if(target['id'] == source['id']){
            var offset = -1;

            for (var i = 0; i < target ['children'].length; i++)
            {
              if(i == 0 && target['children'][i]['id'] == 'author'){
                var offset = 0;
                continue;
              }
              if(target['children'][i]['id'] == el['id']){
                console.log( i - offset);
                this.dataservice.moveGoal(source['id'], i - offset);
                break;
              }
            }
          }else{
            this.dataservice.changeOwner(source['id'], target['id'])
          }

        }
      )
    ); 
  }


  ngOnInit() {
  }
   
  logout(){
  this.dataservice.message = 'Thank You for Using Scrum'
  this.dataservice.logout();
  }
  addGoal(){
    this.dataservice.addGoal();
  }

  ngOnDestroy(){
    this.subs.unsubscribe();
    this.dragula.destroy('mainTable');
  }

  editGoal(event){
    console.log(event);
    var items = event.target.innerText.split(/\)\s(.+)/)
    var goal_name = window.prompt('Editing Task ID #' + items[0] + ':', items[1]);
    if (goal_name == null || goal_name == ''){
      this.dataservice.message = 'Edit Canceled.';
    }else{
      this.http.put('http://' + this.dataservice.domain_name + '/api/scrumgoals/', JSON.stringify({'mode': 1,'goal_id': items[0], 'new_name': goal_name}), this.dataservice.authOptions).subscribe(
    data => {
      this.dataservice.users = data['data'];
      this.dataservice.message = data['message'];
    },
    err =>{
      console.error(err);
      if(err['status'] == 401)
      {
        this.dataservice.message = 'Session Invalid or Expired. Please Login.';
        this.dataservice.logout();
    }else{
      this.dataservice.message = "Unexpected Error";  
    }
    }
    );

    }
  }

  doNothing(){
    console.log("Did no Sh*t");
  }

}


