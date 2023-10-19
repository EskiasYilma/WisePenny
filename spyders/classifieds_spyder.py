try:
    logging.info("{}\n[Automation Started] [{}]".format(str("#"*50), str(datetime.now())))
    main()
    update_files()
    import_ids_processed = []
    # import_ids = [27]
    import_ids = [24, 29, 30, 31, 27, 26, 25, 23]
    random.shuffle(import_ids)
    for i in import_ids:
        if i not in import_ids_processed:
            process_import(str(i))
            import_ids_processed.append(i)
            logging.info("[Processed] {}".format(str(i)))
    logging.info("{}\n[Automation Ended] [{}]".format(str("#"*50), str(datetime.now())))
except Exception as e:
    logging.info(str(e))
    logging.info("{}\n[Automation Interrupted] [{}]".format(str("#"*50), str(datetime.now())))
