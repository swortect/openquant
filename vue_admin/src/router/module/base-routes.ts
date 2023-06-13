import BaseLayout from '../../layouts/BaseLayout.vue';
import Login from '../../views/index/login.vue'; 


export default [
  {
    path: '/',
    redirect: '/list'
  },
  {
    path: '/login',
    component: Login,
    meta: { title: '登录页面' },
  },
  {
    path: '/workspace',
    redirect: '/workspace/workbench',
    component: BaseLayout,
    meta: { title: '工作空间' },
    children: [
      {
        path: '/workspace/workbench',
        name: 'Workbench',
        component: () => import('../../views/workSpace/workbench/index.vue'),
        meta: { title: '工作台', requireAuth: true, affix: true, closable: false },
      },
      {
        path: '/workspace/console',
        component: () => import('../../views/workSpace/console/index.vue'),
        meta: { title: '控制台', requireAuth: true },
      },
      {
        path: '/workspace/analysis',
        component: () => import('../../views/workSpace/analysis/index.vue'),
        meta: { title: '分析页', requireAuth: true },
      }
    ]
  },{
    path: '/error',
    component: BaseLayout,
    meta: { title: '错误页面' },
    children: [
      {
        path: '/error/401',
        component: () => import('../../views/error/401.vue'),
        meta: { title: '401' },
      },
      {
        path: '/error/403',
        component: () => import('../../views/error/403.vue'),
        meta: { title: '403' },
      },
      {
        path: '/error/404',
        component: () => import('../../views/error/404.vue'),
        meta: { title: '404' },
      },
      {
        path: '/error/500',
        component: () => import('../../views/error/500.vue'),
        meta: { title: '500' },
      }
    ]
  },{
    path: '/system',
    component: BaseLayout,
    meta: { title: '系统管理' },
    children: [
      {
        path: '/system/user',
        component: () => import('../../views/system/user/index.vue'),
        meta: { title: '用户管理', requireAuth: true },
      },
      {
        path: '/system/role',
        component: () => import('../../views/system/role/index.vue'),
        meta: { title: '角色管理', requireAuth: true },
      }
    ]
  },{
    path: '/result',
    component: BaseLayout,
    meta: { title: '错误页面' },
    children: [
      {
        path: '/result/success',
        component: () => import('../../views/result/success.vue'),
        meta: { title: '成功页面', requireAuth: true },
      },
      {
        path: '/result/failure',
        component: () => import('../../views/result/failure.vue'),
        meta: { title: '失败页面', requireAuth: true },
      },
    ]
  },{
    path: '/list',
    redirect: '/stock/index',
    component: BaseLayout,
    meta: { title: '列表页面' },
    children: [
      {
        path: '/table/base',
        component: () => import('../../views/table/base.vue'),
        meta: { title: '查询列表', requireAuth: true },
      },

    ]
  },{
    path: '/form',
    component: BaseLayout,
    meta: { title: '表单页面' },
    children: [
      {
        path: '/form/base',
        component: () => import('../../views/form/base.vue'),
        meta: { title: '基础表单', requireAuth: true },
      },
      {
        path: '/form/step',
        component: () => import('../../views/form/step.vue'),
        meta: { title: '分步表单', requireAuth: true },
      },
      {
        path: '/form/intricate',
        name: 'Intricate',
        component: () => import('../../views/form/intricate.vue'),
        meta: { title: '复杂表单', requireAuth: true },
      },
    ]
  },{
    path: '/directive',
    component: BaseLayout,
    meta: { title: '内置指令' },
    children: [
      {
        path: '/directive/permission',
        component: () => import('../../views/directive/permission.vue'),
        meta: { title: '权限指令', requireAuth: true },
      },
    ]
  },{
    path: '/component',
    component: BaseLayout,
    meta: { title: '常用组件' },
    children: [
      {
        path: '/component/qrcode',
        component: () => import('../../views/component/qrcode.vue'),
        meta: { title: '二维码', requireAuth: true },
      },
      {
        path: '/component/barcode',
        component: () => import('../../views/component/barcode.vue'),
        meta: { title: '条形码', requireAuth: true },
      },
      {
        path: '/component/treeSelect',
        component: () => import('../../views/component/treeSelect.vue'),
        meta: { title: '下拉树', requireAuth: true },
      },
    ]
  }
]
