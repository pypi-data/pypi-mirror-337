# -*- coding: utf-8 -*-
# server.py
# Copyright (c) 2025 zedmoster

from contextlib import asynccontextmanager
from typing import AsyncIterator, Dict, Any
from mcp.server.fastmcp import FastMCP
from .revit_connection import RevitConnection
from .tools import *
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RevitMCPServer")

# Global connection for resources
_Revit_connection = None
_polyhaven_enabled = False
_port = 8080


def get_Revit_connection():
    """Get or create a persistent Revit connection"""
    global _Revit_connection, _polyhaven_enabled

    if _Revit_connection is not None:
        try:
            result = _Revit_connection.send_command("get_polyhaven_status")
            _polyhaven_enabled = result.get("enabled", False)
            return _Revit_connection
        except Exception as e:
            logger.warning(f"Existing connection is no longer valid: {str(e)}")
            try:
                _Revit_connection.disconnect()
            except:
                pass
            _Revit_connection = None

    if _Revit_connection is None:
        _Revit_connection = RevitConnection(host="localhost", port=_port)
        if not _Revit_connection.connect():
            logger.error("Failed to connect to Revit")
            _Revit_connection = None
            raise Exception(
                "Could not connect to Revit. Make sure the Revit addon is running.")
        logger.info("Created new persistent connection to Revit")

    return _Revit_connection


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage server startup and shutdown lifecycle"""
    try:
        logger.info("RevitMCP server starting up")
        try:
            Revit = get_Revit_connection()
            logger.info("Successfully connected to Revit on startup")
        except Exception as e:
            logger.warning(f"Could not connect to Revit on startup: {str(e)}")
            logger.warning(
                "Make sure the Revit addon is running before using Revit resources or tools")

        yield {}
    finally:
        global _Revit_connection
        if _Revit_connection:
            logger.info("Disconnecting from Revit on shutdown")
            _Revit_connection.disconnect()
            _Revit_connection = None
        logger.info("RevitMCP server shut down")


# Create the MCP server with lifespan support
mcp = FastMCP(
    "RevitMCP",
    description="Revit integration through the Model Context Protocol",
    lifespan=server_lifespan
)

# Register tools
mcp.tool()(create_levels)
mcp.tool()(create_grids)
mcp.tool()(create_walls)
mcp.tool()(create_floors)
mcp.tool()(create_rooms)
mcp.tool()(create_room_tags)
mcp.tool()(create_family_instances)
mcp.tool()(find_elements)
mcp.tool()(update_elements)
mcp.tool()(delete_elements)
mcp.tool()(parameter_elements)
mcp.tool()(get_location)
mcp.tool()(show_elements)
mcp.tool()(active_view)
mcp.tool()(call_func)


@mcp.prompt()
def asset_creation_strategy() -> str:
    """
    基于现有工具集定义Revit资源(图元、族等)创建和管理的优化策略

    返回:
        str: 包含以下内容的综合策略文档:
            - 图元创建最佳实践
            - 性能优化技术
            - 错误处理方法
            - 批处理建议
            - 资源管理

    策略要点:
        1. 批处理:
           - 利用API工具的批量创建功能
           - 分组相似操作以减少事务
           - 使用已验证参数模式确保一致性

        2. 错误处理:
           - 失败操作的事务回滚
           - 使用标准JSON-RPC错误响应格式
           - 包含详细日志记录

        3. 性能优化:
           - 通过批处理减少Revit API调用
           - 使用字符串格式的元素ID
           - 缓存常用元素引用

        4. 创建工作流:
           - 遵循层级创建顺序(标高→轴网→墙→楼板→族实例)
           - 放置依赖图元前验证宿主存在
           - 使用毫米单位确保一致性

        5. 资源管理:
           - 尽可能重用元素
           - 批量操作使用轻量级表示
           - 操作后清理临时元素

        示例工作流:
            1. 创建必要标高(create_levels)
            2. 添加轴网(create_grids)
            3. 创建墙和结构元素(create_walls)
            4. 添加楼板(create_floors)
            5. 放置门窗族实例(create_family_instances)
            6. 创建房间(create_rooms)
            7. 添加房间标签(create_room_tags)
    """

    strategy = """
    Revit资源创建综合策略
    ====================

    I. 图元创建原则
    ---------------
    1. 层级优先: 先创建宿主元素再创建依赖元素
    2. 批处理: 尽可能使用批量操作
    3. 验证: API调用前验证参数
    4. 事务管理: 分组相关操作

    II. 性能优化
    ------------
    1. 最小化视图切换: 使用元素ID而非激活视图
    2. 缓存引用: 存储常用元素集合
    3. 延迟加载: 仅当需要时查询元素详情
    4. 批量处理: 使用工具中的批量创建函数

    III. 错误处理
    -------------
    1. 使用标准JSON-RPC错误代码
    2. 实现事务回滚点
    3. 包含元素引用的详细日志
    4. 执行前验证参数

    IV. 推荐工作流
    --------------
    1. 建筑工作流:
       - 标高(create_levels) → 轴网(create_grids) → 墙(create_walls) → 楼板(create_floors)→ 门窗(create_family_instances)

    2. 标注工作流:
       - 创建房间(create_rooms) → 添加标签(create_room_tags)
       
    3. 创建族:
       - 查找族类型(find_elements) → 创建族实例(create_family_instances)

    V. 最佳实践
    -----------
    1. 统一使用tools.py中的函数:
       - 创建: create_levels/create_grids/create_walls等
       - 查询: find_elements/parameter_elements
       - 修改: update_elements
       - 删除: delete_elements
       - 特殊: DimensionViewPlanGrids 轴网两道尺寸线

    2. 遵循参数验证模式:
       - 使用字典列表格式参数(确保参数中不要包含注释内容,否则可能无法正确验证)
       - 元素ID统一转为字符串
       - 坐标单位使用毫米

    3. 元素管理:
       - 创建后使用show_elements验证
       - 使用get_location获取定位信息
       - 批量更新使用update_elements

    实施说明:
    - 所有坐标参数必须使用毫米单位
    - 元素ID优先使用字符串格式
    - 放置族实例前用find_elements验证宿主存在
    - 相关操作使用同一事务组
    - 使用active_view管理视图切换
    """

    return strategy


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()
