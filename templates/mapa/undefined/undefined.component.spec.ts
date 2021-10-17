import { TestBed, async } from '@angular/core/testing';

import { undefinedComponent } from './undefined.component';

describe('undefinedComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        undefinedComponent
      ],
    }).compileComponents();
  }));

  it('should create the undefined', async(() => {
    const fixture = TestBed.createComponent(undefinedComponent);
    const undefined = fixture.debugElement.componentInstance;
    expect(undefined).toBeTruthy();
  }));

  it(`should have as title 'undefined'`, async(() => {
    const fixture = TestBed.createComponent(undefinedComponent);
    const undefined = fixture.debugElement.componentInstance;
    expect(undefined.title).toEqual('undefined');
  }));

  it('should render title in a h1 tag', async(() => {
    const fixture = TestBed.createComponent(undefinedComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Welcome to undefined!');
  }));
});
