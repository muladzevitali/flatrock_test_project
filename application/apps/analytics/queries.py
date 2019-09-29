__author__ = "Vitali Muladze"

min_max_avg = {"$group": {"_id": None, "Maximum Compensation": {"$max": "$compensation"},
                          "Minimum Compensation": {"$min": "$compensation"},
                          "Average Compensation": {"$avg": "$compensation"},
                          "Number of Employees": {"$sum": 1}}}

min_max_avg_all_years = {"$group": {"_id": "$year", "Maximum Compensation": {"$max": "$compensation"},
                                    "Minimum Compensation": {"$min": "$compensation"},
                                    "Average Compensation": {"$avg": "$compensation"},
                                    "Number of Employees": {"$sum": 1}}}

avg_department = {"$group": {"_id": "$department",
                             "Average Compensation": {"$avg": "$compensation"},
                             "Number of Employees": {"$sum": 1}}}

avg_department_year = {"$group": {"_id": {"Department": "$department", "Year": "$year"},
                                  "Average Compensation": {"$avg": "$compensation"},
                                  "Number of Employees": {"$sum": 1}}}

avg_department_year_job = {"$group": {"_id": {"Department": "$department", "Year": "$year", "Job": "$job"},
                                      "Average Compensation": {"$avg": "$compensation"},
                                      "Number of Employees": {"$sum": 1}}}

avg_department_job = {"$group": {"_id": {"Department": "$department", "Job": "$job"},
                                 "Average Compensation": {"$avg": "$compensation"},
                                 "Number of Employees": {"$sum": 1}}}

forecast_avg_min_max_department = {"$group": {"_id": {"Department": "$department", "Year": "$year"},
                                              "max": {"$max": "$compensation"},
                                              "min": {"$min": "$compensation"},
                                              "avg": {"$avg": "$compensation"}}}
