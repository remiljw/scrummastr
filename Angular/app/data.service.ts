import { Injectable } from '@angular/core';
import {HttpClient,HttpHeaders} from '@angular/common/http';
import { Router } from '@angular/router';

// const httpOptions = {
//   headers: new HttpHeaders({
//     'Content-Type':  'application/json',
//     'Authorization': 'my-auth-token'
//   })
// };

@Injectable({
  providedIn: 'root'
})
export class DataService {

  public domain_name = '127.0.0.1:8080';


  public username;

  

  public login_username;
  public login_password;

  public role;
  public users;
  public goal_name;
  public goal_id;
  public fullname;
  

  public message;
  public user_fullname = '';
  public user_username;
  public user_email;
  public user_password;
  public user_password_repeat;  
  public user_usertype;
  public httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };
  
  public authOptions;

  constructor(private http: HttpClient, private router: Router,) { }

  
  signup()
  {
    this.http.post('http://' + this.domain_name + '/api/scrumusers/', JSON.stringify({'username':this.user_username,'email': this.user_email,  'password': this.user_password,'pass_auth':this.user_password_repeat, 'full_name': this.user_fullname,'usertype': this.user_usertype}), this.httpOptions).subscribe(
        data => {
            this.message = data['message'];
            this.user_fullname = '';
            this.user_username = '';
            // this.router.navigate(['scrumboard']);
            this.user_email = '';
            this.user_password = '';
            this.user_password_repeat = '';
            this.user_usertype = '';
        },
        err => {
          this.message = 'User Creation Failed! Unexpected Error!';
          console.error(err);
          this.user_fullname = '';
          // this.user_lastname = '';
          this.user_username = '';
          this.user_email = '';
          this.user_password = '';
          this.user_password_repeat = '';
          this.user_usertype = '';

      }
    );
  }
  
  login()
  {
    this.http.post('http://' + this.domain_name + '/api-token-auth/', JSON.stringify({'username': this.login_username, 'password': this.login_password}), this.httpOptions).subscribe(
      data => {
        sessionStorage.setItem('username', this.login_username);
        sessionStorage.setItem('role', data['role']);
        sessionStorage.setItem('token', data['token']);
        this.username = this.login_username;
        this.role = data['role'];
        this.fullname = data['nickname'];
        this.users = data['data'];
        this.message = data['message'];
        this.router.navigate(['scrumboard']);
        this.login_username = '';
        this.login_password = '';
        console.log(data);

        this.authOptions = {
          headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + data['token']})
      };
      },
      err => {
            if(err['status'])
              this.message = 'Login Failed: Invalid Credentials';
            else
              this.message = 'Login Failed: Unexpected.';
            console.error(err);
            this.username = '';
            this.login_username = '';
            this.login_password = '';
      }
    );
  }
  logout()
  {
  this.username = '';
  this.role = '';
  this.users = [];
  this.authOptions = {};
  this.router.navigate(['login']);
  sessionStorage.removeItem('username');
  sessionStorage.removeItem('role');
  sessionStorage.removeItem('token');

  }
  addGoal(){
    this.http.post('http://' + this.domain_name + '/api/scrumgoals/', JSON.stringify({'name':this.goal_name, 'id':this.goal_id}), this.authOptions).subscribe(
    data => {
      this.users = data['data'];
      this.message = data['message'];
      this.goal_name = '';
      this.goal_id='';
    },
    err =>{
      console.error(err); 
      if(err['status'] == 401)
      {
        this.message = 'Session Invalid or Expired. Please Login.';
        this.logout();
    }else{
        this.message = "Unexpected Error";  
    }
    }
    );
  }
  moveGoal(goal_id, to_id){
    this.http.patch('http://' + this.domain_name + '/api/scrumgoals/', JSON.stringify({'goal_id': goal_id, 'to_id': to_id}), this.authOptions).subscribe(
    data => {
     
      this.users = data['data'];
      this.message = data['message'];
    },
    err =>{
      console.error(err);
      if(err['status'] == 401)
      {
        this.message = 'Session Invalid or Expired. Please Login.';
        this.logout();
    }else{
        this.message = "Unexpected Error";  
    }
    }
    );
    
  }

  changeOwner(from_id, to_id){
    this.http.put('http://' + this.domain_name + '/api/scrumgoals/', JSON.stringify({'mode': 0,'from_id': from_id, 'to_id': to_id}), this.authOptions).subscribe(
    data => {
      this.users = data['data'];
      this.message = data['message'];
    },
    err =>{
      console.error(err);
      if(err['status'] == 401)
      {
        this.message = 'Session Invalid or Expired. Please Login.';
        this.logout();
    }else{
        this.message = "Unexpected Error";  
    }
    }
    );

  }

}

  
  
