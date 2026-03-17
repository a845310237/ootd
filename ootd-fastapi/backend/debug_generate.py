#!/usr/bin/env python3
"""Debug script for outfit generation issues."""
import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"

def test_outfit_generation():
    """Test outfit generation with user's exact parameters."""
    print("="*50)
    print("穿搭生成接口调试")
    print("="*50)

    # Test 1: Check if users have clothing data
    print("\n1. 检查用户服装数据...")

    # Try login with test user
    login_data = {
        "username": "testoss@example.com",
        "password": "test123456"
    }

    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)

    if response.status_code != 200:
        print(f"✗ 登录失败: {response.status_code}")
        print(f"  {response.text}")
        return False

    token = response.json()["access_token"]
    print(f"✓ 登录成功")

    # Check clothing data
    headers = {"Authorization": f"Bearer {token}"}
    clothing_response = requests.get(f"{BASE_URL}/clothing", headers=headers)

    if clothing_response.status_code == 200:
        clothing = clothing_response.json()
        print(f"✓ 用户有 {len(clothing)} 件服装")
        for item in clothing:
            print(f"  - {item['name']} ({item['category']})")
    else:
        print(f"✗ 获取服装数据失败: {clothing_response.status_code}")
        return False

    # Test 2: Generate outfit with user's parameters
    print("\n2. 使用用户参数生成穿搭...")

    outfit_data = {
        "style": "休闲",
        "occasion": "日常",
        "season": "春",
        "reference_image": "https://zootd.oss-cn-shanghai.aliyuncs.com/images/2026/03/df449f92-8bdc-4da8-88a7-247ccab8bbda.jpeg"
    }

    print(f"参数: {json.dumps(outfit_data, ensure_ascii=False, indent=2)}")

    try:
        response = requests.post(
            f"{BASE_URL}/outfits/generate",
            headers=headers,
            json=outfit_data,
            timeout=60  # 60 second timeout
        )

        print(f"\n响应状态码: {response.status_code}")

        if response.status_code == 201:
            result = response.json()
            print("✓ 穿搭生成成功！")
            print(f"  穿搭ID: {result['id']}")
            print(f"  风格: {result['style']}")
            print(f"  场合: {result['occasion']}")
            print(f"  季节: {result['season']}")
            print(f"  AI生成图片: {result['result_url'][:80]}...")
            print(f"  包含服装: {len(result['items'])} 件")
            return True

        elif response.status_code == 400:
            error = response.json()
            print(f"✗ 请求参数错误:")
            print(f"  {error.get('detail', 'Unknown error')}")
            return False

        elif response.status_code == 401:
            print(f"✗ 认证失败，请重新登录")
            return False

        elif response.status_code == 500:
            print(f"✗ 服务器内部错误")
            print(f"  {response.text}")
            return False

        else:
            print(f"✗ 未知错误: {response.status_code}")
            print(f"  {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("✗ 请求超时，可能是因为:")
        print("  - 参考图片下载时间过长")
        print("  - MiniMax API响应慢")
        print("  - 网络连接问题")
        return False

    except Exception as e:
        print(f"✗ 请求异常: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_outfit_generation()

    print("\n" + "="*50)
    if success:
        print("✓ 测试成功！接口工作正常。")
        print("如果您仍然遇到问题，请检查:")
        print("1. 使用的用户账号是否有服装数据")
        print("2. Token是否有效（可能需要重新登录）")
        print("3. 网络连接是否正常")
    else:
        print("✗ 测试失败。请检查上述错误信息。")
    print("="*50)

    sys.exit(0 if success else 1)
