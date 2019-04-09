import { Component, OnInit } from '@angular/core';
import { Routes, RouterModule, Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  welcome = 'Welcome to remiljwscrum Homepage';
  constructor(
    private router: Router
    ) { }


  signUp() {
    this.router.navigate(['signup']);
  }
  logIn() {
    this.router.navigate(['login']);
  }
  ngOnInit() {
  }

}