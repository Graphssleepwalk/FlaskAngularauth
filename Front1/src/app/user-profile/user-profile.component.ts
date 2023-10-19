import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {
  user: any;  // Define a user object to store the user data

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    // Fetch user information when the component initializes
    this.userService.getUserInfo().subscribe(
      (data) => {
        this.user = data;  // Assign the user data to the 'user' object
      },
      (error) => {
        console.error('Error fetching user information:', error);
      }
    );
  }
}