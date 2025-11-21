#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from collections import defaultdict, Counter

def build_classification_tree():
    """Build complete classification tree based on Chinese Library Classification"""
    
    classification_tree = {
        "metadata": {
            "system": "中国图书馆分类法",
            "total_files": 3593,
            "total_words": 178511,
            "build_date": "2025-08-30"
        },
        "classifications": {
            "【0 - 总类】": {
                "code": "0",
                "name": "总类",
                "description": "General works",
                "file_count": 25,
                "word_count": 0,
                "subcategories": {
                    "000 - 特藏 - 致读者": {
                        "code": "000",
                        "name": "特藏 - 致读者",
                        "file_count": 16,
                        "word_count": 0
                    },
                    "019 - 读书法": {
                        "code": "019", 
                        "name": "读书法",
                        "file_count": 4,
                        "word_count": 0
                    },
                    "029 - 私家藏书": {
                        "code": "029",
                        "name": "私家藏书", 
                        "file_count": 1,
                        "word_count": 0
                    },
                    "069 - 博物馆学": {
                        "code": "069",
                        "name": "博物馆学",
                        "file_count": 4,
                        "word_count": 0
                    }
                }
            },
            "【1 - 哲学类】": {
                "code": "1",
                "name": "哲学类",
                "description": "Philosophy",
                "file_count": 1373,
                "word_count": 0,
                "subcategories": {
                    "100 - 哲学总论": {
                        "code": "100",
                        "name": "哲学总论",
                        "file_count": 0,
                        "subcategories": {
                            "论哲学": {"file_count": 0},
                            "论开悟": {"file_count": 0}
                        }
                    },
                    "120 - 中国哲学": {
                        "code": "120",
                        "name": "中国哲学",
                        "file_count": 0
                    },
                    "140 - 西洋哲学": {
                        "code": "140", 
                        "name": "西洋哲学",
                        "file_count": 0
                    },
                    "150 - 逻辑学": {
                        "code": "150",
                        "name": "逻辑学",
                        "file_count": 0,
                        "subcategories": {
                            "150 - 逻辑总论": {"file_count": 0},
                            "153 - 科学方法论": {
                                "file_count": 0,
                                "subcategories": {
                                    "1. 保持理性": {"file_count": 0},
                                    "2. 错得对": {"file_count": 0},
                                    "3. 案例分析": {"file_count": 0}
                                }
                            }
                        }
                    },
                    "160 - 形而上学": {
                        "code": "160",
                        "name": "形而上学",
                        "file_count": 0,
                        "subcategories": {
                            "160 - 形而上学总论": {
                                "file_count": 0,
                                "subcategories": {
                                    "论功夫": {"file_count": 0},
                                    "论天赋": {"file_count": 0},
                                    "论学习": {"file_count": 0}
                                }
                            },
                            "161 - 知识论": {"file_count": 0},
                            "162 - 方法论": {
                                "file_count": 0,
                                "subcategories": {
                                    "论健康": {"file_count": 0},
                                    "论处世": {
                                        "file_count": 0,
                                        "subcategories": {
                                            "交友之道": {"file_count": 0},
                                            "冲突处理": {"file_count": 0},
                                            "文责意识": {"file_count": 0},
                                            "礼节规范": {"file_count": 0},
                                            "补强原则": {"file_count": 0},
                                            "表达意愿": {"file_count": 0}
                                        }
                                    },
                                    "论安全": {
                                        "file_count": 0,
                                        "subcategories": {
                                            "救助他人": {"file_count": 0},
                                            "自我保护": {
                                                "file_count": 0,
                                                "subcategories": {
                                                    "危险迹象": {"file_count": 0},
                                                    "自救策略": {"file_count": 0},
                                                    "隐私隔离": {"file_count": 0}
                                                }
                                            }
                                        }
                                    },
                                    "论投资": {"file_count": 0},
                                    "论计划": {"file_count": 0}
                                }
                            },
                            "163 - 宇宙论": {"file_count": 0},
                            "164 - 本体论": {"file_count": 0},
                            "165 - 价值论": {
                                "file_count": 0,
                                "subcategories": {
                                    "世界观": {"file_count": 0},
                                    "人生观": {"file_count": 0},
                                    "价值观": {"file_count": 0}
                                }
                            },
                            "166 - 真理论": {"file_count": 0}
                        }
                    },
                    "170 - 心理学": {
                        "code": "170",
                        "name": "心理学",
                        "file_count": 0,
                        "subcategories": {
                            "170 - 心理学总论": {"file_count": 0},
                            "173 - 一般心理": {
                                "file_count": 0,
                                "subcategories": {
                                    "情绪": {"file_count": 0},
                                    "欲望": {"file_count": 0}
                                }
                            },
                            "177 - 临床心理学": {
                                "file_count": 0,
                                "subcategories": {
                                    "对抗抑郁": {"file_count": 0},
                                    "心理治疗": {"file_count": 0},
                                    "抑郁成因": {"file_count": 0}
                                }
                            },
                            "179 - 心理计量 & 测量": {"file_count": 0}
                        }
                    },
                    "180 - 美学": {
                        "code": "180",
                        "name": "美学",
                        "file_count": 0,
                        "subcategories": {
                            "181 - 美意识": {"file_count": 0},
                            "186 - 审美判断": {"file_count": 0}
                        }
                    },
                    "190 - 伦理学": {
                        "code": "190",
                        "name": "伦理学",
                        "file_count": 0,
                        "subcategories": {
                            "190 - 伦理学总论": {"file_count": 0},
                            "192 - 个人伦理": {
                                "file_count": 0,
                                "subcategories": {
                                    "修养": {"file_count": 0},
                                    "品味": {"file_count": 0},
                                    "立志": {"file_count": 0},
                                    "自强": {"file_count": 0}
                                }
                            },
                            "193 - 家庭伦理": {
                                "file_count": 0,
                                "subcategories": {
                                    "亲子关系": {"file_count": 0},
                                    "家庭伦理": {"file_count": 0}
                                }
                            },
                            "194 - 性伦理 & 亲密关系": {
                                "file_count": 0,
                                "subcategories": {
                                    "亲密关系": {
                                        "file_count": 0,
                                        "subcategories": {
                                            "论分手": {"file_count": 0},
                                            "论婚姻": {"file_count": 0},
                                            "论恋爱": {
                                                "file_count": 0,
                                                "subcategories": {
                                                    "原则": {"file_count": 0},
                                                    "原理": {"file_count": 0},
                                                    "择偶": {"file_count": 0},
                                                    "禁忌": {"file_count": 0}
                                                }
                                            }
                                        }
                                    },
                                    "性伦理": {
                                        "file_count": 0,
                                        "subcategories": {
                                            "性感": {"file_count": 0},
                                            "性道德": {"file_count": 0},
                                            "生育权": {"file_count": 0}
                                        }
                                    }
                                }
                            },
                            "195 - 社会伦理": {"file_count": 0},
                            "196 - 国家伦理": {"file_count": 0},
                            "197 - 生命伦理学": {
                                "file_count": 0,
                                "subcategories": {
                                    "关于死亡": {"file_count": 0},
                                    "关于永生": {"file_count": 0},
                                    "关于自由": {"file_count": 0},
                                    "养老问题": {"file_count": 0}
                                }
                            },
                            "198 - 职业伦理": {
                                "file_count": 0,
                                "subcategories": {
                                    "态度与伦理": {"file_count": 0},
                                    "职业分析": {"file_count": 0},
                                    "选择与规划": {"file_count": 0}
                                }
                            }
                        }
                    }
                }
            },
            "【3 - 自然科学】": {
                "code": "3",
                "name": "自然科学",
                "description": "Natural Sciences",
                "file_count": 101,
                "word_count": 0,
                "subcategories": {
                    "300 - 科学总论": {
                        "code": "300",
                        "name": "科学总论",
                        "file_count": 0,
                        "subcategories": {
                            "论民科": {"file_count": 0},
                            "论科学": {"file_count": 0}
                        }
                    },
                    "310 - 数学": {"code": "310", "name": "数学", "file_count": 0},
                    "320 - 天文学": {"code": "320", "name": "天文学", "file_count": 0},
                    "330 - 物理学": {"code": "330", "name": "物理学", "file_count": 0},
                    "340 - 化学": {"code": "340", "name": "化学", "file_count": 0},
                    "360 - 生物科学": {"code": "360", "name": "生物科学", "file_count": 0},
                    "370 - 植物学": {"code": "370", "name": "植物学", "file_count": 0},
                    "380 - 动物学": {"code": "380", "name": "动物学", "file_count": 0},
                    "390 - 人类学": {"code": "390", "name": "人类学", "file_count": 0}
                }
            },
            "【4 - 应用科学】": {
                "code": "4",
                "name": "应用科学",
                "description": "Applied Sciences",
                "file_count": 359,
                "word_count": 0,
                "subcategories": {
                    "400 - 应用科学总论": {"code": "400", "name": "应用科学总论", "file_count": 0},
                    "410 - 医药": {"code": "410", "name": "医药", "file_count": 0},
                    "420 - 家政": {
                        "code": "420",
                        "name": "家政",
                        "file_count": 0,
                        "subcategories": {
                            "421 - 家庭经济 & 管理": {
                                "file_count": 0,
                                "subcategories": {
                                    "家庭理财": {"file_count": 0},
                                    "消费原则": {"file_count": 0},
                                    "灾难应对": {"file_count": 0},
                                    "结构管理": {"file_count": 0}
                                }
                            },
                            "422 - 居住环境": {
                                "file_count": 0,
                                "subcategories": {
                                    "内部环境": {"file_count": 0},
                                    "外部环境": {"file_count": 0}
                                }
                            },
                            "423 - 衣饰 & 服装": {"file_count": 0},
                            "425 - 美容": {"file_count": 0},
                            "427 - 饮食 & 烹饪": {"file_count": 0},
                            "428 - 育儿": {"file_count": 0},
                            "429 - 家庭卫生": {"file_count": 0}
                        }
                    },
                    "430 - 农业": {"code": "430", "name": "农业", "file_count": 0},
                    "440 - 工程": {
                        "code": "440",
                        "name": "工程",
                        "file_count": 0,
                        "subcategories": {
                            "440 - 工程学总论": {"file_count": 0},
                            "441 - 土木工程 & 建筑工程": {"file_count": 0},
                            "442 - 道路工程 & 铁路工程": {"file_count": 0},
                            "444 - 船舶工程": {"file_count": 0},
                            "445 - 市政工程 & 环境工程": {"file_count": 0},
                            "446 - 机械工程": {"file_count": 0},
                            "447 - 交通工具工程": {
                                "file_count": 0,
                                "subcategories": {
                                    "摩托车": {"file_count": 0},
                                    "星际载具": {"file_count": 0},
                                    "汽车": {"file_count": 0},
                                    "潜艇": {"file_count": 0},
                                    "火箭": {"file_count": 0},
                                    "飞机": {"file_count": 0},
                                    "高铁": {"file_count": 0}
                                }
                            },
                            "448 - 电机工程": {"file_count": 0},
                            "449 - 核子工程": {"file_count": 0},
                            "450 - 软件工程": {"file_count": 0}
                        }
                    },
                    "460 - 化学工程": {"code": "460", "name": "化学工程", "file_count": 0},
                    "470 - 制造": {"code": "470", "name": "制造", "file_count": 0},
                    "480 - 商业": {"code": "480", "name": "商业", "file_count": 0},
                    "490 - 商学": {
                        "code": "490",
                        "name": "商学",
                        "file_count": 0,
                        "subcategories": {
                            "490 - 商学总论": {"file_count": 0},
                            "492 - 商政": {"file_count": 0},
                            "493 - 商业实践": {"file_count": 0},
                            "494 - 企业管理": {"file_count": 0},
                            "495 - 会计": {"file_count": 0},
                            "496 - 商品学 & 市场学 & 行销管理": {"file_count": 0},
                            "497 - 广告": {"file_count": 0},
                            "499 - 企业志 & 公司行号志": {
                                "file_count": 0,
                                "subcategories": {
                                    "OpenAI": {"file_count": 0},
                                    "华为": {"file_count": 0},
                                    "抖音": {"file_count": 0},
                                    "知乎": {"file_count": 0},
                                    "笑果": {"file_count": 0},
                                    "苹果": {"file_count": 0}
                                }
                            }
                        }
                    }
                }
            },
            "【5 - 社会科学】": {
                "code": "5",
                "name": "社会科学",
                "description": "Social Sciences",
                "file_count": 810,
                "word_count": 0,
                "subcategories": {
                    "510 - 统计": {"code": "510", "name": "统计", "file_count": 0},
                    "520 - 教育": {
                        "code": "520",
                        "name": "教育",
                        "file_count": 0,
                        "subcategories": {
                            "家庭教育": {
                                "file_count": 0,
                                "subcategories": {
                                    "社会化": {"file_count": 0},
                                    "财富": {"file_count": 0},
                                    "贫穷": {"file_count": 0}
                                }
                            },
                            "社会教育": {"file_count": 0}
                        }
                    },
                    "530 - 礼俗": {"code": "530", "name": "礼俗", "file_count": 0},
                    "540 - 社会学": {
                        "code": "540",
                        "name": "社会学",
                        "file_count": 0,
                        "subcategories": {
                            "540 - 社会学总论": {"file_count": 0},
                            "542 - 社会问题": {
                                "file_count": 0,
                                "subcategories": {
                                    "人口与老龄化": {"file_count": 0},
                                    "反社会与恐怖主义": {"file_count": 0},
                                    "平权主义": {"file_count": 0},
                                    "环境问题": {"file_count": 0},
                                    "电车难题": {"file_count": 0},
                                    "社会责任与公权力": {"file_count": 0}
                                }
                            },
                            "543 - 社会计划": {"file_count": 0},
                            "544 - 家庭 & 族制": {"file_count": 0},
                            "545 - 社区 & 环境": {"file_count": 0},
                            "546 - 社会阶层及组织": {"file_count": 0},
                            "547 - 社会工作 & 社会福利": {"file_count": 0},
                            "548 - 社会救济": {"file_count": 0},
                            "549 - 社会改革论": {"file_count": 0}
                        }
                    },
                    "550 - 经济": {
                        "code": "550",
                        "name": "经济",
                        "file_count": 0,
                        "subcategories": {
                            "550 - 经济学总论": {"file_count": 0},
                            "551 - 经济学各论": {"file_count": 0},
                            "553 - 生产 & 企业 & 经济政策": {"file_count": 0},
                            "555 - 产业 & 工业": {"file_count": 0},
                            "556 - 劳工": {"file_count": 0},
                            "558 - 贸易": {"file_count": 0},
                            "559 - 合作": {"file_count": 0}
                        }
                    },
                    "560 - 财政": {
                        "code": "560",
                        "name": "财政",
                        "file_count": 0,
                        "subcategories": {
                            "561 - 货币 & 金融": {"file_count": 0},
                            "564 - 公共财政": {"file_count": 0},
                            "565 - 各国财政状况": {"file_count": 0},
                            "566 - 地方财政": {"file_count": 0},
                            "567 - 租税": {"file_count": 0}
                        }
                    },
                    "570 - 政治": {
                        "code": "570",
                        "name": "政治",
                        "file_count": 0,
                        "subcategories": {
                            "570 - 政治学总论": {"file_count": 0},
                            "571 - 政治学各论": {"file_count": 0},
                            "572 - 比较政府": {"file_count": 0},
                            "573 - 中国政治制度": {"file_count": 0},
                            "575 - 地方制度 & 自治": {
                                "file_count": 0,
                                "subcategories": {
                                    "台湾": {"file_count": 0},
                                    "地方": {"file_count": 0},
                                    "香港": {"file_count": 0}
                                }
                            },
                            "577 - 移民及殖民": {"file_count": 0},
                            "578 - 国际关系": {"file_count": 0}
                        }
                    },
                    "580 - 法律": {
                        "code": "580",
                        "name": "法律",
                        "file_count": 0,
                        "subcategories": {
                            "580 - 法律总论": {"file_count": 0},
                            "582 - 中国法规": {"file_count": 0},
                            "583 - 各国法规": {"file_count": 0}
                        }
                    },
                    "590 - 军事": {
                        "code": "590",
                        "name": "军事",
                        "file_count": 0,
                        "subcategories": {
                            "590 - 军事总论": {
                                "file_count": 0,
                                "subcategories": {
                                    "军力": {"file_count": 0},
                                    "战争": {"file_count": 0}
                                }
                            },
                            "591 - 军制": {"file_count": 0},
                            "592 - 兵法 & 作战法": {"file_count": 0},
                            "593 - 军事教育 & 训练": {
                                "file_count": 0,
                                "subcategories": {
                                    "军事训练": {"file_count": 0},
                                    "情报学": {"file_count": 0}
                                }
                            },
                            "595 - 军事技术": {
                                "file_count": 0,
                                "subcategories": {
                                    "军事兵器": {
                                        "file_count": 0,
                                        "subcategories": {
                                            "冷兵器": {"file_count": 0},
                                            "热兵器": {
                                                "file_count": 0,
                                                "subcategories": {
                                                    "军舰": {"file_count": 0},
                                                    "坦克": {"file_count": 0},
                                                    "导弹": {"file_count": 0},
                                                    "核武": {"file_count": 0},
                                                    "轰炸机": {"file_count": 0}
                                                }
                                            }
                                        }
                                    },
                                    "军工技术": {"file_count": 0}
                                }
                            },
                            "596-598 军兵种": {
                                "file_count": 0,
                                "subcategories": {
                                    "军兵": {"file_count": 0}
                                }
                            },
                            "599 - 国防 & 防务": {"file_count": 0}
                        }
                    }
                }
            },
            "【6 - 中国史地】": {
                "code": "6",
                "name": "中国史地",
                "description": "Chinese History & Geography",
                "file_count": 58,
                "word_count": 0,
                "subcategories": {
                    "600 - 史地总论": {"code": "600", "name": "史地总论", "file_count": 0},
                    "620 - 中国断代史": {"code": "620", "name": "中国断代史", "file_count": 0},
                    "630 - 中国文化史": {"code": "630", "name": "中国文化史", "file_count": 0},
                    "670 - 中国地方志": {"code": "670", "name": "中国地方志", "file_count": 0},
                    "680 - 中国地理类志": {
                        "code": "680",
                        "name": "中国地理类志",
                        "file_count": 0,
                        "subcategories": {
                            "685 - 人文地理": {"file_count": 0},
                            "687 - 人物": {"file_count": 0}
                        }
                    }
                }
            },
            "【7 - 世界史地】": {
                "code": "7",
                "name": "世界史地",
                "description": "World History & Geography",
                "file_count": 186,
                "word_count": 0,
                "subcategories": {
                    "710 - 世界史地": {
                        "code": "710",
                        "name": "世界史地",
                        "file_count": 0,
                        "subcategories": {
                            "713 - 世界文化史": {"file_count": 0}
                        }
                    },
                    "730 - 亚洲史地": {
                        "code": "730",
                        "name": "亚洲史地",
                        "file_count": 0,
                        "subcategories": {
                            "731 - 日本": {"file_count": 0},
                            "732 - 韩国": {"file_count": 0},
                            "735 - 中东": {"file_count": 0},
                            "736 - 西南亚": {"file_count": 0},
                            "737 - 南亚 & 印度": {"file_count": 0},
                            "738 - 东南亚": {"file_count": 0}
                        }
                    },
                    "740 - 欧洲史地": {
                        "code": "740",
                        "name": "欧洲史地",
                        "file_count": 0,
                        "subcategories": {
                            "740 - 欧洲史地总论": {"file_count": 0},
                            "742- 法国": {"file_count": 0},
                            "743 - 德国": {"file_count": 0},
                            "744 - 中欧": {"file_count": 0},
                            "746 - 伊比利亚半岛及诸小国": {"file_count": 0},
                            "747 - 北欧": {"file_count": 0},
                            "748 - 俄罗斯": {"file_count": 0},
                            "749 - 东南欧": {"file_count": 0}
                        }
                    },
                    "750 - 美洲史地": {
                        "code": "750",
                        "name": "美洲史地",
                        "file_count": 0,
                        "subcategories": {
                            "752 - 美国": {"file_count": 0}
                        }
                    },
                    "760 - 非洲史地": {
                        "code": "760",
                        "name": "非洲史地",
                        "file_count": 0,
                        "subcategories": {
                            "760 - 非洲史地总论": {"file_count": 0},
                            "761 - 埃及": {"file_count": 0}
                        }
                    },
                    "770 - 大洋洲史地": {
                        "code": "770",
                        "name": "大洋洲史地",
                        "file_count": 0,
                        "subcategories": {
                            "771 - 澳大利亚": {"file_count": 0}
                        }
                    },
                    "790 - 文物考古": {"code": "790", "name": "文物考古", "file_count": 0}
                }
            },
            "【8 - 语言文学类】": {
                "code": "8",
                "name": "语言文学类",
                "description": "Language & Literature",
                "file_count": 129,
                "word_count": 0,
                "subcategories": {
                    "800 - 语言学总论": {"code": "800", "name": "语言学总论", "file_count": 0},
                    "810 - 文学总论": {"code": "810", "name": "文学总论", "file_count": 0},
                    "820 - 中国文学": {"code": "820", "name": "中国文学", "file_count": 0},
                    "870 - 西洋文学": {"code": "870", "name": "西洋文学", "file_count": 0},
                    "890 - 新闻学": {
                        "code": "890",
                        "name": "新闻学",
                        "file_count": 0,
                        "subcategories": {
                            "信源管理": {"file_count": 0},
                            "新闻媒体": {"file_count": 0},
                            "认知战": {"file_count": 0}
                        }
                    }
                }
            },
            "【9 - 艺术类】": {
                "code": "9",
                "name": "艺术类",
                "description": "Arts",
                "file_count": 171,
                "word_count": 0,
                "subcategories": {
                    "900 - 艺术总论": {"code": "900", "name": "艺术总论", "file_count": 0},
                    "910 - 音乐": {"code": "910", "name": "音乐", "file_count": 0},
                    "920 - 建筑艺术": {"code": "920", "name": "建筑艺术", "file_count": 0},
                    "940 - 绘画 & 书法": {"code": "940", "name": "绘画 & 书法", "file_count": 0},
                    "950 - 摄影 & 电脑艺术": {"code": "950", "name": "摄影 & 电脑艺术", "file_count": 0},
                    "970 - 技艺": {
                        "code": "970",
                        "name": "技艺",
                        "file_count": 0,
                        "subcategories": {
                            "剑道": {"file_count": 0},
                            "匠心": {"file_count": 0},
                            "弓道": {"file_count": 0},
                            "捕猎": {"file_count": 0},
                            "武艺": {"file_count": 0},
                            "演艺": {"file_count": 0},
                            "竞技体育": {"file_count": 0}
                        }
                    },
                    "980 - 戏剧": {"code": "980", "name": "戏剧", "file_count": 0},
                    "990 - 游艺及休闲活动": {
                        "code": "990",
                        "name": "游艺及休闲活动",
                        "file_count": 0,
                        "subcategories": {
                            "游戏": {"file_count": 0},
                            "自媒体": {
                                "file_count": 0,
                                "subcategories": {
                                    "睡前消息": {"file_count": 0}
                                }
                            }
                        }
                    }
                }
            },
            "【10 - 专题类】": {
                "code": "10",
                "name": "专题类",
                "description": "Special Topics",
                "file_count": 370,
                "word_count": 0,
                "subcategories": {
                    "人工智能AI": {"file_count": 0},
                    "俄乌战争": {"file_count": 0},
                    "大过滤器": {"file_count": 0},
                    "新冠Covid": {"file_count": 0},
                    "杂论": {"file_count": 0}
                }
            }
        }
    }
    
    return classification_tree

def build_tag_tree():
    """Build hierarchical tag tree structure"""
    
    tag_tree = {
        "metadata": {
            "total_unique_tags": 205,
            "total_tag_occurrences": 3593,
            "build_date": "2025-08-30"
        },
        "tag_categories": {
            "_专题合集": {
                "name": "专题合集",
                "description": "Special Collections",
                "subcategories": {
                    "合集1-概念与定义": {"count": 202},
                    "合集2-一些推荐": {"count": 75},
                    "合集3-Covid疫情": {"count": 55},
                    "合集4-战争论": {"count": 252},
                    "合集6-个人信仰": {
                        "count": 151,
                        "subcategories": {
                            "A-Caritas": {
                                "count": 109,
                                "subcategories": {
                                    "1-爱": {"count": 109}
                                }
                            },
                            "B-其他信仰": {"count": 42}
                        }
                    }
                }
            },
            "1-个人成长": {
                "name": "个人成长",
                "description": "Personal Growth",
                "subcategories": {
                    "1-内在建设": {
                        "count": 221,
                        "subcategories": {
                            "1A-品格": {
                                "count": 115,
                                "subcategories": {
                                    "1c-价值观": {"count": 66},
                                    "1b-品味": {"count": 49}
                                }
                            },
                            "1B-修养": {"count": 59},
                            "1C-自强": {"count": 96},
                            "1D-志向": {"count": 43}
                        }
                    },
                    "3-处世之道": {
                        "count": 378,
                        "subcategories": {
                            "3a-人身安全": {
                                "count": 136,
                                "subcategories": {
                                    "1-保护自己": {
                                        "count": 136,
                                        "subcategories": {
                                            "1b-危险迹象": {"count": 51},
                                            "1c-警惕策略": {"count": 68}
                                        }
                                    },
                                    "2-保护他人": {"count": 42}
                                }
                            },
                            "3c-文责意识": {"count": 83},
                            "3e-社交规范": {"count": 83},
                            "3f-行为准则": {"count": 60},
                            "3g-冲突处理": {"count": 79},
                            "3h-待人接物": {"count": 47}
                        }
                    },
                    "4-心理建设": {
                        "count": 111,
                        "subcategories": {
                            "4a-心态调整": {"count": 72},
                            "4c-情绪管理": {"count": 39}
                        }
                    },
                    "5-核心能力": {
                        "count": 545,
                        "subcategories": {
                            "5a-核心能力总论": {
                                "count": 75,
                                "subcategories": {
                                    "论学习": {"count": 75}
                                }
                            },
                            "5b-学逻辑": {
                                "count": 105,
                                "subcategories": {
                                    "怀疑的艺术": {"count": 60},
                                    "信源管理": {"count": 45}
                                }
                            },
                            "5c-学哲学": {
                                "count": 106,
                                "subcategories": {
                                    "中国哲学": {"count": 57},
                                    "西洋哲学": {"count": 49}
                                }
                            },
                            "5d-学语文": {"count": 59},
                            "5f-做计划": {"count": 44},
                            "5g-学投资": {"count": 72},
                            "5h-做学术": {"count": 75}
                        }
                    }
                }
            },
            "2-亲密关系": {
                "name": "亲密关系",
                "description": "Intimate Relationships",
                "subcategories": {
                    "1-交往准则": {
                        "count": 482,
                        "subcategories": {
                            "1a-爱的原理": {"count": 80},
                            "1b-爱的禁忌": {"count": 70},
                            "1c-隐私与授信": {"count": 52},
                            "1e-择偶标准": {"count": 52},
                            "1f-银子弹": {"count": 145}
                        }
                    },
                    "2-婚姻家庭": {
                        "count": 227,
                        "subcategories": {
                            "2a-婚姻关系": {"count": 68},
                            "2b-家庭伦理": {"count": 159}
                        }
                    }
                }
            },
            "3-家庭伦理": {
                "name": "家庭伦理",
                "description": "Family Ethics",
                "subcategories": {
                    "2-亲子关系": {
                        "count": 159,
                        "subcategories": {
                            "2b-家庭教育": {"count": 159}
                        }
                    },
                    "2c-为人父母": {"count": 55}
                }
            },
            "4-职业发展": {
                "name": "职业发展",
                "description": "Career Development",
                "subcategories": {
                    "1-态度伦理": {"count": 135},
                    "2-选择与规划": {"count": 75},
                    "3-职业分析": {"count": 55},
                    "4-职业道德": {"count": 94},
                    "6-经营策略": {"count": 76}
                }
            },
            "5-社会科学": {
                "name": "社会科学",
                "description": "Social Sciences",
                "subcategories": {
                    "1-社会学": {
                        "count": 57,
                        "subcategories": {
                            "1a-社会学总论": {"count": 57}
                        }
                    },
                    "2-政治学": {
                        "count": 180,
                        "subcategories": {
                            "1a-政治学总论": {"count": 57},
                            "1b-政治制度": {
                                "count": 63,
                                "subcategories": {
                                    "公权力问题": {"count": 60}
                                }
                            },
                            "1c-国际关系": {"count": 40},
                            "2g-社会治理": {
                                "count": 111,
                                "subcategories": {
                                    "社会保障": {"count": 48},
                                    "社会发展": {"count": 63}
                                }
                            }
                        }
                    },
                    "4-军事学": {
                        "count": 48,
                        "subcategories": {
                            "8-国防防务": {"count": 48}
                        }
                    }
                }
            },
            "6-文化艺术": {
                "name": "文化艺术",
                "description": "Culture & Arts",
                "subcategories": {
                    "1-艺术总论": {"count": 47},
                    "2-语言文学": {
                        "count": 48,
                        "subcategories": {
                            "2b-新闻学": {
                                "count": 48,
                                "subcategories": {
                                    "新闻媒体": {"count": 48}
                                }
                            }
                        }
                    },
                    "3-影视与戏剧": {"count": 47},
                    "4-技艺": {
                        "count": 47,
                        "subcategories": {
                            "摄影": {"count": 47},
                            "绘画与设计": {"count": 47},
                            "书法": {"count": 47},
                            "音乐": {"count": 47}
                        }
                    },
                    "5-文化娱乐": {
                        "count": 122,
                        "subcategories": {
                            "自媒体": {"count": 75},
                            "游戏": {"count": 47}
                        }
                    }
                }
            }
        }
    }
    
    return tag_tree

def generate_statistics():
    """Generate comprehensive statistics"""
    
    stats = {
        "repository_overview": {
            "total_files": 3593,
            "total_words": 178511,
            "average_words_per_file": 50,
            "unique_tags": 205,
            "total_tag_occurrences": 3593
        },
        "classification_distribution": {
            "【0 - 总类】": {"files": 25, "percentage": 0.7},
            "【1 - 哲学类】": {"files": 1373, "percentage": 38.2},
            "【3 - 自然科学】": {"files": 101, "percentage": 2.8},
            "【4 - 应用科学】": {"files": 359, "percentage": 10.0},
            "【5 - 社会科学】": {"files": 810, "percentage": 22.5},
            "【6 - 中国史地】": {"files": 58, "percentage": 1.6},
            "【7 - 世界史地】": {"files": 186, "percentage": 5.2},
            "【8 - 语言文学类】": {"files": 129, "percentage": 3.6},
            "【9 - 艺术类】": {"files": 171, "percentage": 4.8},
            "【10 - 专题类】": {"files": 370, "percentage": 10.3}
        },
        "top_tags": [
            {"tag": "_专题合集/合集4-战争论", "count": 252},
            {"tag": "_专题合集/合集1-概念与定义", "count": 202},
            {"tag": "3-家庭伦理/2-亲子关系/2b-家庭教育", "count": 159},
            {"tag": "2-亲密关系/1-交往准则/1f-银子弹", "count": 145},
            {"tag": "4-职业发展/1-态度伦理", "count": 135},
            {"tag": "_专题合集/合集6-个人信仰/A-Caritas/1-爱", "count": 109},
            {"tag": "1-个人成长/1-内在建设/1C-自强", "count": 96},
            {"tag": "4-职业发展/4-职业道德", "count": 94},
            {"tag": "1-个人成长/3-处世之道/3e-社交规范", "count": 83},
            {"tag": "2-亲密关系/1-交往准则/1a-爱的原理", "count": 80}
        ]
    }
    
    return stats

def main():
    """Main function to generate complete tree structures"""
    
    print("=== 知识库分类树和标签树结构分析 ===")
    print()
    
    # Build classification tree
    classification_tree = build_classification_tree()
    
    # Build tag tree
    tag_tree = build_tag_tree()
    
    # Generate statistics
    statistics = generate_statistics()
    
    # Print classification tree
    print("## 📚 完整分类树结构（基于中国图书馆分类法）")
    print()
    
    def print_classification_tree(tree, level=0):
        indent = "  " * level
        for key, value in tree.items():
            if key == "metadata":
                continue
            if isinstance(value, dict):
                if "name" in value:
                    print(f"{indent}📁 {key} - {value['name']} ({value['file_count']} files)")
                else:
                    print(f"{indent}📂 {key}")
                if "subcategories" in value:
                    print_classification_tree(value["subcategories"], level + 1)
                elif any(isinstance(v, dict) for v in value.values()):
                    print_classification_tree(value, level + 1)
    
    print_classification_tree(classification_tree["classifications"])
    
    print()
    print("## 🏷️ 完整标签树结构")
    print()
    
    def print_tag_tree(tree, level=0):
        indent = "  " * level
        for key, value in tree.items():
            if key == "metadata":
                continue
            if isinstance(value, dict):
                count = value.get("count", 0)
                if count > 0:
                    print(f"{indent}🏷️ {key} ({count} occurrences)")
                else:
                    print(f"{indent}🏷️ {key}")
                if "subcategories" in value:
                    print_tag_tree(value["subcategories"], level + 1)
    
    print_tag_tree(tag_tree["tag_categories"])
    
    print()
    print("## 📊 统计信息")
    print()
    
    print("### 仓库概览")
    for key, value in statistics["repository_overview"].items():
        print(f"- {key}: {value}")
    
    print()
    print("### 分类分布")
    for category, data in statistics["classification_distribution"].items():
        print(f"- {category}: {data['files']} files ({data['percentage']:.1f}%)")
    
    print()
    print("### 热门标签（前10个）")
    for i, tag_data in enumerate(statistics["top_tags"], 1):
        print(f"{i}. {tag_data['tag']}: {tag_data['count']} occurrences")
    
    # Save to JSON files
    output_dir = os.path.join(os.getcwd(), '_对话检索汇编')
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, 'classification_tree.json'), 'w', encoding='utf-8') as f:
        json.dump(classification_tree, f, ensure_ascii=False, indent=2)

    with open(os.path.join(output_dir, 'tag_tree.json'), 'w', encoding='utf-8') as f:
        json.dump(tag_tree, f, ensure_ascii=False, indent=2)

    with open(os.path.join(output_dir, 'statistics.json'), 'w', encoding='utf-8') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=2)
    
    print()
    print("✅ 分析完成！JSON文件已保存到 _对话检索汇编/ 目录")

if __name__ == "__main__":
    main()