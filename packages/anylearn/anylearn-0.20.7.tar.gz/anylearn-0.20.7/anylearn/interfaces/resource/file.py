import os
from datetime import datetime
from typing import Optional, Union

from anylearn.utils.api import url_base, get_with_token
from anylearn.utils.errors import AnyLearnException
from anylearn.interfaces.resource.resource import Resource

class File(Resource):
    """
    AnyLearn其他文件类，以方法映射文件CRUD相关接口
    
    Attributes
    ----------
    id
        文件的唯一标识符，自动生成，由FILE+uuid1生成的编码中后28个有效位（小写字母和数字）组成（自动生成）
    name
        文件的名称（长度1~50）
    description
        文件描述（长度最大255）
    state
        文件状态
    public
        文件是否公开（默认为False）
    upload_time
        文件上传时间
    filename
        下一步中会被分片上传的文件的完整文件名（包括扩展名）（长度1~128）
    is_zipfile
        是否为zip文件
    file_path
        文件文件路径
    size
        文件大小
    creator_id
        创建者ID
    node_id
        文件节点ID
    load_detail
        初始化时是否加载详情
    """

    """具体资源信息配置"""
    _fields = {
        # 资源创建/更新请求包体中必须包含且不能为空的字段
        'required': {
            'create': ['name', 'filename'],
            'update': ['id', 'name'],
        },
        # 资源创建/更新请求包体中包含的所有字段
        'payload': {
            'create': ['name', 'description', 'public',
                       'filename'],
            'update': ['id', 'name', 'description', 'public'],
        },
    }
    """
    创建/更新对象时：

    - 必须包含且不能为空的字段 :obj:`_fields['required']`
    - 所有字段 :obj:`_fields['payload']`
    """

    def __init__(self,
                 id: Optional[str]=None,
                 name: Optional[str]=None,
                 description: Optional[str]=None,
                 state: Optional[int]=None,
                 public=False,
                 upload_time: Optional[Union[datetime, str]]=None,
                 filename: Optional[str]=None,
                 is_zipfile: Optional[int]=None,
                 file_path: Optional[Union[str, bytes, os.PathLike]]=None,
                 size: Optional[str]=None,
                 creator_id: Optional[str]=None,
                 node_id: Optional[str]=None,
                 load_detail=False):
        """
        Parameters
        ----------
        id
            文件的唯一标识符，自动生成，由FILE+uuid1生成的编码中后28个有效位（小写字母和数字）组成（自动生成）
        name
            文件的名称（长度1~50）
        description
            文件描述（长度最大255）
        state
            文件状态
        public
            文件是否公开（默认为False）
        upload_time
            文件上传时间
        filename
            下一步中会被分片上传的文件的完整文件名（包括扩展名）（长度1~128）
        is_zipfile
            是否为zip文件
        file_path
            文件文件路径
        size
            文件大小
        creator_id
            创建者ID
        node_id
            文件节点ID
        load_detail
            初始化时是否加载详情
        """
        super().__init__(id=id, name=name, description=description,
                         state=state, public=public,
                         upload_time=upload_time, filename=filename,
                         is_zipfile=is_zipfile, file_path=file_path, size=size,
                         creator_id=creator_id, node_id=node_id,
                         load_detail=load_detail)

    @classmethod
    def get_list(cls) -> list:
        """
        获取文件列表
        
        Returns
        -------
        List [File]
            文件集合。
        """
        res = get_with_token(f"{url_base()}/file/list")
        if res is None or not isinstance(res, list):
            raise AnyLearnException("请求未能得到有效响应")
        return [
            File(id=f['id'], name=f['name'], description=f['description'],
                 state=f['state'], public=f['public'],
                 upload_time=f['upload_time'], filename=f['filename'],
                 creator_id=f['creator_id'], node_id=f['node_id'])
            for f in res
        ]

    def get_detail(self):
        """
        获取文件详细信息

        - 对象属性 :obj:`id` 应为非空

        Returns
        -------
        File
            文件对象。
        """
        self._check_fields(required=['id'])
        res = get_with_token(f"{url_base()}/file/query",
                             params={'id': self.id})
        if not res or not isinstance(res, list):
            raise AnyLearnException("请求未能得到有效响应")
        res = res[0]
        self.__init__(id=res['id'], name=res['name'],
                      description=res['description'], state=res['state'],
                      public=res['public'],
                      upload_time=res['upload_time'], filename=res['filename'],
                      is_zipfile=True if res['is_zipfile'] == 1 else False,
                      file_path=res['file'], size=res['size'],
                      creator_id=res['creator_id'], node_id=res['node_id'])

    def _namespace(self):
        return "file"
