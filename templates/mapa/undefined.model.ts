import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';

// 组件
import { undefinedComponent } from './undefined/undefined.component';

// 定义常量 路由
const routes: any = [
    {
        path: 'undefined',
        component: undefinedComponent
    }
];

@NgModule({
    imports: [
        RouterModule.forChild(routes)
    ],
    providers: [],
    declarations: [undefinedComponent]
})
export class undefinedModule {}