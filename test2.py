def for_loop(a,b,c):
	input_detail2 = a
	jogai_shiyo_cf = b
	jogai_size_block_no = c

	for i in range(2):
		for j in range(len(jogai_size_block_no[i])):
			input_detail2[3] = jogai_shiyo_cf[i]
			input_detail2[4] = jogai_size_block_no[i][j]
			print(input_detail2)



input_detail2 = ['54', '540','5000','6F', '0', '1','トムズイリン']
jogai_shiyo_cf = ['6G', 'SG']
jogai_size_block_no = [[11, 10, 12],
					   [10]]

for_loop(input_detail2, jogai_shiyo_cf, jogai_size_block_no)


print("#########")
input_detail2 = ['60', '600','5000','6F', '0', '1','トムズイリン']
jogai_shiyo_cf = ['6G', 'SG']
jogai_size_block_no = [[8, 9, 10, 11],
					   [6, 7, 8, 9, 10]]

for_loop(input_detail2, jogai_shiyo_cf, jogai_size_block_no)