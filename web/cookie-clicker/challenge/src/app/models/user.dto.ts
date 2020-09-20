import {IsEmail, IsNotEmpty, IsNumber} from "class-validator";

export class UserDto {

  @IsNotEmpty()
  @IsEmail()
  email: string;

  @IsNotEmpty()
  password: string;
}

export class User {

  @IsNotEmpty()
  uid: string;

  @IsNotEmpty()
  @IsEmail()
  email: string;

  // @IsNumber()
  cookieCount?: any

}
