import { Component, OnInit } from '@angular/core';
import { Routes, RouterModule, Router } from '@angular/router';
import { DataService } from './../data.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private router: Router, public dataservice: DataService ) { }

  ngOnInit() {
  }
  signup() {
    this.dataservice.signup();
  }
  toLogin()
  {
    this.router.navigate(['login']);
    this.dataservice.message = '';
  }

}


