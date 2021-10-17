import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { undefinedComponent } from './undefined.component';

@NgModule({
  declarations: [
    undefinedComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [undefinedComponent]
})
export class undefinedModule { }
