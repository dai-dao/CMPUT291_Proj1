SELECT staff_id,  drug_name,  sum(amount) * (strftime("%d", strftime("%d", MIN (end_med, "2016-09-05") - MAX(start_med, "2016-08-05"))  )) as Total
FROM medications
GROUP BY staff_id, drug_name;



select cat.category, cat.drug_name, sub.Total where cat.drug_name in

(SELECT drug_name,  (sum(amount) * (strftime("%d", strftime("%d", MIN (end_med, "2016-09-05") - MAX(start_med, "2016-08-05"))  )) )AS Total
FROM medications
GROUP BY drug_name) as sub


from drugs cat order by cat.category;